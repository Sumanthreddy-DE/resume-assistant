# STATE — resume-assistant

Type: project
Status: active
Last touched: 2026-11-28

<!-- Machine-maintained by /save-session Step 6b. Do not hand-edit rows or dates. -->

## What

FastAPI + Anthropic backend for "Fragen an meinen Lebenslauf" on sumanthreddy.de: answers recruiters from a fixed corpus plus one read-only GitHub tool.

## Doing

- Nothing in progress. Question log collects real visitor questions (on since 2026-11-27).

## Resume here

- Around 2026-12-05: review the question log (`question-log-review`), then run one full eval and grade it; that run also checks prompt `364896d` and closes `document-mentions-and-email-pointers`. Handoff: harness/sessions/resume-assistant/2026-11-28-colleague-tone-evals-session.tmp

## Pipeline

- See BACKLOG.md.

## Landmines

- The Rostock entry is never added to the corpus (user's explicit exception).
- A corpus pushed after a restart loads only after the 1-hour TTL or another restart.

## Done

- 2026-11-28 — colleague tone (`e461864`), date-aware periods, source-line rewrite (`9c5906e`), answer-language hint (`70dbdac`), question log on; full run 24 OK, 5 partial, 0 FAIL (`84f50e7`); prompt `364896d` deployed.
