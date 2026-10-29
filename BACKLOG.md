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

_(none)_

---

## Open — S2 (UX gap, polish, deferred decisions)

_(none)_

---

## Open — S3 (tech debt, deprecations, low-impact polish)

_(none yet)_

---

## Doing

_(items currently being worked — move from Open when started, back to Open if paused.)_

---

## Done this session (2026-10-29)

- **branch-divergence-main-vs-feat-repo-tool** — resolved: `feat/repo-tool` fast-forwarded into
  `main`, pushed and deployed on the VPS at `6a5714b`; live check (T4) passed 2026-10-29.
- **tool-simready-de-german-source-line** — fixed deterministically in the site's client, not the
  prompt: `assets/chat.js` `fixSourceLang()` (Sumanthreddy-DE.github.io `6b1a500`). The prompt
  attempt `fb061b2` was reverted unevaluated (`4943e59`).
- **eval-rerun-after-commit-message-removal** — won't do: the v6 result file stays the historical
  record of what the model saw then; it is hand-graded 18/18 bestanden (`5e27d2d`).
- **eval-runner-tool-recording** — `evals/run_eval.py` now collects tool events, adds the
  `expect_tool` field and the relative-time flag, plus a Tools column. `5b70242`
- **eval-three-tool-cases** — `tool-simready-de`, `tool-pinn-en`, `tool-injection` added;
  15 → 18 cases, 52 → 55 tests. `5b70242`
- **strip-commit-messages-from-model** — `fetch_repo` no longer returns
  `last_commit_message`; tests assert no key containing `message`; README documents why. `6a5714b`

---

## Archived (older sweeps, compressed)

_(empty — populates over time as one-line entries per sweep.)_
