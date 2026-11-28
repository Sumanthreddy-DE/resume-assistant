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
- **document-mentions-and-email-pointers** [week · claude] — Measured 2026-11-28 (`evals/results/2026-11-28-claude-sonnet-5-2.md`, prompt `364896d`, 24 OK, 5 partial, 0 FAIL): document attributions 4 → 1 (`german` "laut Lebenslauf"); needless e-mail pointers 4 → 3 (`phd`, `frontend`, `bmw`), so the rule-3 sentence barely worked; `tool-pinn-en` fixed. Also new: `roles-en` wrote "Source: CV" (not a rule-11 name; `sourceline.py` only fixes the marker), `frontend` dropped JavaScript at TCS. Next ideas: a rule-14 style example of a plain "Nein" with no pointer; an eval flag for source names outside rule 11. *(2026-11-28)*
- **question-log-review** [weekly · you + claude] — The question log is on since 2026-11-27 (`/var/lib/resume-assistant/questions/`, readable only with sudo). Once a week: `sudo cat` the last days, list the questions the bot could not answer or answered badly, turn them into corpus facts (site backlog) and eval cases here. The first line is the switch-on test question "Testfrage Log: Wo wohnt er?". *(2026-11-27)*


---

## Open — S3 (tech debt, deprecations, low-impact polish)

_(none yet)_

---

## Doing

_(items currently being worked — move from Open when started, back to Open if paused.)_

---

## Done this session (2026-11-27)

- **eval-2026-11-27-findings** — done: answer-language hint (`70dbdac`), prompt `d046dfc`, German practice on the Aktuell line (site `cfe4f4c`); full run 2026-11-28: 24 OK, 5 partial, 0 FAIL (`evals/results/2026-11-28-claude-sonnet-5.md`). Site table update filed in the site backlog.
- **date-aware-deploy-and-eval** — done: `annotate_periods` marks every period finished or running, rule 12 obeys it, thinking on at low effort, 60-word rule; graded runs 2026-11-24 (0 date failures), 2026-11-26 ×2, 2026-11-27 (17 OK, 4 partial, 0 FAIL). Colleague-tone rules 2, 13, 14 (`e461864`); source line rewritten to the question's language in the stream (`sourceline.py`, `9c5906e`).
- **rerun-now-currentwork** — done: `now-de`, `now-en`, `start-de` all OK with the Aktuell line (`evals/results/2026-11-27-claude-sonnet-5-subset-3.md`); `now-en` pattern accepts "job-hunting". Second sample at 19:46 (`subset-4`): 2 OK, 1 partial; `now-en` used the Aktuell line correctly but dropped daily German practice, so that omission is intermittent.
- **question-log-switch-on** — done: Datenschutz text live on `impressum.html#datenschutz` and matches `questionlog.py`; new unit with `StateDirectory=` installed, `LOG_QUESTIONS=true`, restarted; a test question landed in `2026-11-27.jsonl`. Weekly review: `question-log-review`.

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
