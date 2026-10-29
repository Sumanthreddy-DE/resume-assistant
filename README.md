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
- **Streaming** as NDJSON: zero or more `delta` / `tool` events, then exactly one `done`
  or `fallback`. A `done` event carries `tools`, the number of tool calls in that answer.
- **The page never depends on this server.** Timeout, rate limit, daily cap or kill
  switch → the page shows a prepared answer with a status line, never an error box.

## Grounding

Rules (in [`system_prompt.md`](system_prompt.md)): facts only from the sources; marked
inference; "not documented" never becomes "no experience"; employer vs. cooperation
partner kept apart; visitor claims and earlier turns cannot change the rules; third
person; a source line under every answer. The corpus is generated from an allowlist of
CV fields, so a new private field cannot leak by default.

## Tool

One read-only tool, `get_repo_activity` ([`tools.py`](tools.py)): description, stars, last
push and latest commit of a public project, so "is SimReady still active?" is answered
from live data instead of a frozen corpus.

- **Allowlist, not free text.** The input schema is an enum of three repository names.
  The model can only pick one of them; anything else is rejected as `unknown repo` before
  a request is made. The URL is built from a literal owner plus that checked value, so no
  text the model or a visitor produces ever reaches a request path.
- **Unauthenticated GitHub REST, 5 s timeout, hourly cache** per repo. Failures are not
  cached and never raise: the answer continues from the corpus and the visitor gets a
  `status: "error"` tool event.
- **At most two tool rounds**, then the next call passes `tool_choice: {"type": "none"}`
  so a model that keeps asking cannot loop. Tool results are data, never instructions.
- **Commit messages are deliberately not passed to the model.** They are the only
  third-party text that would reach it, and they can carry private notes (e.g. job
  application names); the tool returns sha, date and repo metadata only.
- The tool definition rides along on every model call. A question that uses it costs up
  to three API calls (two model rounds plus the tool itself) but still counts as one
  question against the daily cap; the cached system block keeps the re-read cheap.

## Eval

15 fixed questions ([`evals/questions.json`](evals/questions.json)), hand-graded, re-run
after every prompt change. They include traps (Siemens was a cooperation partner, not an
employer), made-up claims, prompt injection through the history and a positive control.
Results: [`evals/results/`](evals/results/).

## Cost and abuse controls

`max_tokens` 600 per round · question ≤ 500 characters · body ≤ 16 KiB · 6 turns of
history · 10 questions per 10 minutes per IP · global daily cap (a tool question makes up
to 3 API calls but still counts as one) · a dedicated API key with a spend limit · kill
switch `BOT_ENABLED`.

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
