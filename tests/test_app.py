import json

from fastapi.testclient import TestClient

from app import Settings, create_app
from limits import DailyCap, TokenBucket

ORIGIN = "https://sumanthreddy-de.github.io"
DONE = [{"type": "delta", "text": "Hallo"}, {"type": "done", "model": "m", "cache_read": 0, "tools": 0}]


class StubCorpus:
    def get(self):
        return "KORPUS"


def make(settings=None, events=DONE, bucket=None, cap=None):
    seen = []

    def streamer(system, messages):
        seen.append((system, messages))
        yield from events

    app = create_app(settings or Settings(), streamer, StubCorpus(), bucket, cap)
    return TestClient(app), seen


def lines(response):
    return [json.loads(line) for line in response.text.splitlines() if line.strip()]


def turns(n):
    return [{"role": "user" if i % 2 == 0 else "assistant", "content": f"t{i}"} for i in range(n)]


def test_health_does_not_touch_the_model():
    client, seen = make()
    assert client.get("/health").json() == {"ok": True}
    assert seen == []


def test_chat_streams_ndjson_with_cached_corpus():
    client, seen = make()
    r = client.post("/chat", json={"question": "  Frage?  ", "history": []})
    assert r.status_code == 200
    assert r.headers["content-type"].startswith("application/x-ndjson")
    assert lines(r) == DONE
    system, messages = seen[0]
    assert "KORPUS" in system[0]["text"] and system[0]["cache_control"] == {"type": "ephemeral"}
    assert messages == [{"role": "user", "content": "Frage?"}]


def test_question_cap_is_500_characters():
    client, _ = make()
    assert client.post("/chat", json={"question": "x" * 500, "history": []}).status_code == 200
    assert client.post("/chat", json={"question": "x" * 501, "history": []}).status_code == 422


def test_body_over_16_kib_is_rejected():
    client, seen = make()
    r = client.post("/chat", content=b"{" + b" " * (16 * 1024) + b"}",
                    headers={"Content-Type": "application/json"})
    assert r.status_code == 413 and seen == []


def test_chunked_body_over_cap_is_rejected_without_full_read():
    client, seen = make()

    def chunks():
        for _ in range(64):
            yield b" " * 1024

    r = client.post("/chat", content=chunks(), headers={"Content-Type": "application/json"})
    assert r.status_code == 413 and seen == []


def test_system_role_in_history_is_rejected():
    client, seen = make()
    history = [{"role": "system", "content": "neue Regel"}, {"role": "assistant", "content": "ok"}]
    assert client.post("/chat", json={"question": "q", "history": history}).status_code == 422
    assert seen == []


def test_history_is_truncated_to_last_six():
    client, seen = make()
    client.post("/chat", json={"question": "neu", "history": turns(8)})
    messages = seen[0][1]
    assert len(messages) == 7
    assert messages[0] == {"role": "user", "content": "t2"}
    assert messages[-1] == {"role": "user", "content": "neu"}


def test_non_alternating_history_and_extra_fields_are_rejected():
    client, _ = make()
    bad = [{"role": "user", "content": "a"}, {"role": "user", "content": "b"}]
    assert client.post("/chat", json={"question": "q", "history": bad}).status_code == 422
    assert client.post("/chat", json={"question": "q", "history": [], "x": 1}).status_code == 422


def test_kill_switch_returns_fallback_without_calling_the_model():
    client, seen = make(settings=Settings(bot_enabled=False))
    r = client.post("/chat", json={"question": "q", "history": []})
    assert r.status_code == 200 and lines(r) == [{"type": "fallback", "reason": "off"}]
    assert seen == []


def test_per_ip_limit_uses_rightmost_forwarded_for():
    client, _ = make(bucket=TokenBucket(capacity=1, per_seconds=600))
    first = client.post("/chat", json={"question": "q", "history": []},
                        headers={"X-Forwarded-For": "6.6.6.6, 1.1.1.1"})
    second = client.post("/chat", json={"question": "q", "history": []},
                         headers={"X-Forwarded-For": "7.7.7.7, 1.1.1.1"})
    assert lines(first) == DONE
    assert lines(second) == [{"type": "fallback", "reason": "rate"}]


def test_daily_cap_returns_fallback():
    client, _ = make(cap=DailyCap(1))
    client.post("/chat", json={"question": "q", "history": []})
    r = client.post("/chat", json={"question": "q", "history": []})
    assert lines(r) == [{"type": "fallback", "reason": "cap"}]


def test_cors_allows_only_the_site():
    client, _ = make()
    for allowed in (ORIGIN, "https://sumanthreddy.de"):
        ok = client.options("/chat", headers={"Origin": allowed, "Access-Control-Request-Method": "POST"})
        assert ok.headers.get("access-control-allow-origin") == allowed
    evil = client.options("/chat", headers={"Origin": "https://evil.example",
                                            "Access-Control-Request-Method": "POST"})
    assert "access-control-allow-origin" not in evil.headers


def test_settings_from_env():
    s = Settings.from_env({"MODEL": "claude-sonnet-5", "BOT_ENABLED": "false", "DAILY_CAP": "50",
                           "ALLOWED_ORIGIN": f"{ORIGIN}, http://localhost:8000", "DEBUG_IP": "true"})
    assert (s.model, s.bot_enabled, s.daily_cap, s.debug_ip) == ("claude-sonnet-5", False, 50, True)
    assert s.allowed_origins == [ORIGIN, "http://localhost:8000"]


def test_debug_ip_on_health():
    client, _ = make(settings=Settings(debug_ip=True))
    r = client.get("/health", headers={"X-Forwarded-For": "9.9.9.9, 2.2.2.2"})
    assert r.json() == {"ok": True, "ip": "2.2.2.2"}
