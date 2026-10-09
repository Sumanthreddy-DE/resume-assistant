"""HTTP layer: POST /chat (streamed NDJSON), GET /health, CORS and request caps."""
import json
import os
from dataclasses import dataclass, field
from typing import Literal

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel, ConfigDict, Field, ValidationError

from answer import CorpusCache, build_system, stream_answer
from limits import DailyCap, TokenBucket

MAX_BODY = 16 * 1024
MAX_TURNS = 6
SITE_ORIGIN = "https://sumanthreddy-de.github.io"
STREAM_HEADERS = {"Cache-Control": "no-store", "X-Accel-Buffering": "no"}


@dataclass
class Settings:
    model: str = "claude-haiku-4-5"
    bot_enabled: bool = True
    daily_cap: int = 200
    allowed_origins: list = field(default_factory=lambda: [SITE_ORIGIN])
    debug_ip: bool = False

    @classmethod
    def from_env(cls, env=os.environ):
        def flag(name, default):
            return env.get(name, default).strip().lower() == "true"
        return cls(
            model=env.get("MODEL", "claude-haiku-4-5").strip(),
            bot_enabled=flag("BOT_ENABLED", "true"),
            daily_cap=int(env.get("DAILY_CAP", "200")),
            allowed_origins=[o.strip() for o in env.get("ALLOWED_ORIGIN", SITE_ORIGIN).split(",") if o.strip()],
            debug_ip=flag("DEBUG_IP", "false"),
        )


class Turn(BaseModel):
    model_config = ConfigDict(extra="forbid")
    role: Literal["user", "assistant"]
    content: str = Field(min_length=1, max_length=4000)


class ChatRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    question: str = Field(min_length=1, max_length=500)
    history: list[Turn] = Field(default_factory=list, max_length=40)


class HistoryError(ValueError):
    pass


def build_messages(req):
    turns = req.history[-MAX_TURNS:]
    while turns and turns[0].role != "user":
        turns = turns[1:]
    expected = "user"
    for turn in turns:
        if turn.role != expected:
            raise HistoryError("history must alternate user/assistant")
        expected = "assistant" if expected == "user" else "user"
    if expected != "user":
        raise HistoryError("history must end with an assistant turn")
    question = req.question.strip()
    if not question:
        raise HistoryError("empty question")
    return [{"role": t.role, "content": t.content} for t in turns] + [{"role": "user", "content": question}]


def client_ip(request):
    # Caddy replaces an X-Forwarded-For sent by an untrusted client with the address it
    # saw, and the rightmost entry is the one a visitor cannot forge either way.
    # Verified on the deployed server in Task 14, Step 6.
    forwarded = request.headers.get("x-forwarded-for", "")
    if forwarded:
        return forwarded.split(",")[-1].strip()
    return request.client.host if request.client else "unknown"


def ndjson(events):
    for event in events:
        yield json.dumps(event, ensure_ascii=False) + "\n"


def stream(events):
    return StreamingResponse(ndjson(events), media_type="application/x-ndjson", headers=STREAM_HEADERS)


def create_app(settings, streamer, corpus, bucket=None, cap=None):
    bucket = bucket or TokenBucket()
    cap = cap or DailyCap(settings.daily_cap)
    app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
    app.add_middleware(CORSMiddleware, allow_origins=settings.allowed_origins,
                       allow_methods=["GET", "POST"], allow_headers=["Content-Type"])

    @app.get("/health")
    async def health(request: Request):
        body = {"ok": True}
        if settings.debug_ip:
            body["ip"] = client_ip(request)
        return body

    @app.post("/chat")
    async def chat(request: Request):
        declared = request.headers.get("content-length", "")
        if declared.isdigit() and int(declared) > MAX_BODY:
            return JSONResponse({"detail": "body too large"}, status_code=413)
        raw = await request.body()
        if len(raw) > MAX_BODY:
            return JSONResponse({"detail": "body too large"}, status_code=413)
        try:
            messages = build_messages(ChatRequest.model_validate_json(raw))
        except (ValidationError, HistoryError):
            return JSONResponse({"detail": "invalid request"}, status_code=422)
        if not settings.bot_enabled:
            return stream([{"type": "fallback", "reason": "off"}])
        if not bucket.allow(client_ip(request)):
            return stream([{"type": "fallback", "reason": "rate"}])
        if not cap.allow():
            return stream([{"type": "fallback", "reason": "cap"}])
        return stream(streamer(build_system(corpus.get()), messages))

    return app


def get_app():
    import anthropic

    settings = Settings.from_env()
    client = anthropic.Anthropic(timeout=30.0)
    corpus = CorpusCache()
    corpus.refresh()

    def streamer(system, messages):
        return stream_answer(client, settings.model, system, messages)

    return create_app(settings, streamer, corpus)
