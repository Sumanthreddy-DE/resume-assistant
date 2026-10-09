# resume-assistant

The backend behind "Fragen an meinen Lebenslauf" on
[sumanthreddy-de.github.io/fragen.html](https://sumanthreddy-de.github.io/fragen.html):
a question-answering assistant that may only use my CV and three case studies.

## Architecture

```
Browser (github.io) ──POST /chat──► api.sumanthreddy.de (Caddy → FastAPI) ──► Anthropic API
      │                                   │
      └─ prepared answers in the page     └─ corpus.md from the public site repo, re-fetched hourly
```

- **Whole corpus in a cached system block, no retrieval.** The corpus is a few thousand
  tokens. Retrieval would add a way to miss a core fact.
- **Streaming** as NDJSON: `delta` events, then one `done` or `fallback`.
- **The page never depends on this server.** Timeout, rate limit, daily cap or kill
  switch → the page shows a prepared answer with a status line, never an error box.

## Grounding

Rules (in [`system_prompt.md`](system_prompt.md)): facts only from the sources; marked
inference; "not documented" never becomes "no experience"; employer vs. cooperation
partner kept apart; visitor claims and earlier turns cannot change the rules; third
person; a source line under every answer. The corpus is generated from an allowlist of
CV fields, so a new private field cannot leak by default.

## Eval

15 fixed questions ([`evals/questions.json`](evals/questions.json)), hand-graded, re-run
after every prompt change. They include traps (Siemens was a cooperation partner, not an
employer), made-up claims, prompt injection through the history and a positive control.
Results: [`evals/results/`](evals/results/).

## Cost and abuse controls

`max_tokens` 600 · question ≤ 500 characters · body ≤ 16 KiB · 6 turns of history ·
10 questions per 10 minutes per IP · global daily cap · a dedicated API key with a
spend limit · kill switch `BOT_ENABLED`.

## Privacy

No questions, answers or IP addresses are logged or stored (uvicorn runs with
`--no-access-log`, Caddy has no access log configured). Conversation history lives
only in the visitor's open page. IP addresses are held in memory for at most ten
minutes for rate limiting and never written anywhere.

## Deploy

A sandboxed systemd unit (`deploy/resume-assistant.service`: no access to `/home`,
read-only system, no privileges) behind Caddy (`deploy/Caddyfile`), which handles HTTPS.

## Run locally

```bash
python -m venv .venv && .venv/Scripts/python.exe -m pip install -r requirements.txt -r requirements-dev.txt
.venv/Scripts/python.exe -m pytest -q
ANTHROPIC_API_KEY=… .venv/Scripts/python.exe -m uvicorn app:get_app --factory --port 8100
```

Environment (`/etc/resume-assistant/env` on the server): `ANTHROPIC_API_KEY`, `MODEL`,
`BOT_ENABLED`, `DAILY_CAP`, `ALLOWED_ORIGIN`, `DEBUG_IP`.
