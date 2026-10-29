# resume-assistant Backlog

Living list of open issues, deferred work, and known caveats. Updated each session.

**Severity rubric**
- **S1** — blocker / data loss / broken demo. Fix before next ship.
- **S2** — UX gap, missing polish, deferred decision.
- **S3** — tech debt, deprecations, low-impact polish, dead code.

**Conventions**
- New issue → append to correct severity section.
- Mention by short slug in commit body (e.g. "Closes: my-issue-slug").
- On close → move to **Done this session** with commit SHA.
- End of session → user sweeps **Done** → **Archived** (one-line compress).
- Last swept: **2026-10-29** (initialised).

---

## Open — S1 (blocker / broken demo)

- **branch-divergence-main-vs-feat-repo-tool** (found 2026-10-29, resume-assistant session) —
  `main` and `feat/repo-tool` both point at `6a5714b`, while each per-commit hook line
  reported `3 ahead of origin` on `feat/repo-tool` only. Establish whether the tool
  commits (`8fa3f0f`, `aaadb8d`, `5b70242`, `6a5714b`) are meant to land on `main` and
  whether `origin/main` should carry them. Next action: `git -C <repo> log --oneline
  origin/main -3` plus a decision on the intended integration path before any push.

---

## Open — S2 (UX gap, polish, deferred decisions)

- **eval-rerun-after-commit-message-removal** (found 2026-10-29, resume-assistant session) —
  `evals/results/2026-10-28-claude-sonnet-5-prompt-v6.md` contains a `tool-pinn-en` answer
  quoting *"updating the license references to Apache 2.0"*, which `6a5714b` makes
  impossible to reproduce (commit messages no longer reach the model). Re-run the eval so
  the result file matches the shipped tool. Next action: local uvicorn on 127.0.0.1:8100,
  `evals/run_eval.py --url http://127.0.0.1:8100`, new dated result file.

- **tool-simready-de-german-source-line** (found 2026-10-29, resume-assistant session) —
  The German `tool-simready-de` answer ended with `Quelle: GitHub (live queried)` instead of
  `live abgefragt`. Rule 17 carries the English value in parentheses and the model copied
  it; no auto-flag catches a wrong-language source line. Next action: decide whether to
  tighten rule 17's wording or add an auto-flag for a `queried` token in German answers,
  then re-grade that row.

---

## Open — S3 (tech debt, deprecations, low-impact polish)

_(none yet)_

---

## Doing

_(items currently being worked — move from Open when started, back to Open if paused.)_

---

## Done this session (2026-10-29)

- **eval-runner-tool-recording** — `evals/run_eval.py` now collects tool events, adds the
  `expect_tool` field and the relative-time flag, plus a Tools column. `5b70242`
- **eval-three-tool-cases** — `tool-simready-de`, `tool-pinn-en`, `tool-injection` added;
  15 → 18 cases, 52 → 55 tests. `5b70242`
- **strip-commit-messages-from-model** — `fetch_repo` no longer returns
  `last_commit_message`; tests assert no key containing `message`; README documents why. `6a5714b`

---

## Archived (older sweeps, compressed)

_(empty — populates over time as one-line entries per sweep.)_
