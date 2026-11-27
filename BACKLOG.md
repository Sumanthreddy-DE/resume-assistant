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

- **date-aware-deploy-and-eval** — the bot read every finished period as current ("Right now he is working on his master's… running to August 2026", live, 2026-11-23): it had no date and rule 12 told it not to know one. Fixed on `fix/date-aware-answers`: today's date in an uncached system block after the corpus, rule 12 compares periods with it, three eval cases (`now-de`, `now-en`, `ended-role`). Live run 2026-11-24 (`30106fb`): 3 FAIL (phd, now-de, now-en): the date alone did not stop Sonnet 5 calling the 08/2026 tutor job and master current, and the auto checks missed all three. Second fix: `annotate_periods` marks every period "· abgeschlossen" or "· laufend" in code; rule 12 obeys the marker; checks tightened with the live answers as negative controls; `run_eval.py --only` for subset runs, never overwriting a result. Open: deploy, subset run, then full 21-case graded run. Corpus side (missing freelance entry, job status, generator drift) is filed in the site backlog as `chat-corpus-drift-and-job-status`. *(found 2026-11-23)*
- **question-log-switch-on** — opt-in question log built (`questionlog.py`, `LOG_QUESTIONS`, default off; text only, emails and phones redacted, date + follow-up flag, 90-day retention, `StateDirectory=` in the unit). Switch on only after the site's Datenschutz page describes it (site backlog `recruiter-questions-and-case-studies`): install the new unit file, add `LOG_QUESTIONS=true` to `/etc/resume-assistant/env`, restart, ask one question, check `/var/lib/resume-assistant/questions/`. Then review the log weekly and turn unanswered questions into corpus facts and eval cases. *(found 2026-11-23)*

---

## Open — S2 (UX gap, polish, deferred decisions)
- **eval-2026-11-27-findings** [week · claude] — Full run after the six-case-study prompt (`evals/results/2026-11-27-claude-sonnet-5-2.md`, 24 OK, 4 partial, 1 FAIL, Sumanth confirmed): (1) `start-en` answered an English question in German; `sourceline.py` fixes only the source line, so the answer language needs a fix in the prompt or the stream. (2) `siemens-en`, `history-injection`, `strongest-en` over 60 words; `history-injection` lists freelance work among employers. (3) `frontend` misses JavaScript at TCS. (4) Eval harness: `pinn-accuracy` pattern misses "5 Prozent"; `start` and `start-de` ask the same question (merge or rephrase one). After fixes, rerun and update the site's `fragen.html` table and the run line on `projekte/lebenslauf-assistent.html`. *(found 2026-11-27, claude-lab session)*


---

## Open — S3 (tech debt, deprecations, low-impact polish)

_(none yet)_

---

## Doing

_(items currently being worked — move from Open when started, back to Open if paused.)_

---

## Done this session (2026-11-15)

- **corpus-and-fragen-stale-facts** — done: corpus synced with the site (SimReady case study rewritten, 2.272 parts; PINN particle-reinforced) in `652b801`, `3bf0ee6`; positive control expects 2.272; FE-tools answer and 18-question count fixed on the site (`3f8bc1a`). Eval re-run live against `https://api.sumanthreddy.de`, hand-graded 18/18 (`c1b526a`, two check patterns fixed). The live chat answered 2.272 after the push.

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
