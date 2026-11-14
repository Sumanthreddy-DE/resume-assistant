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

### corpus-and-fragen-stale-facts
Found by the 2026-11-14 portfolio review (site repo plan
`docs/exec-plans/active/2026-11-14-portfolio-review-fixes.md`, item E). The chat answers from
`corpus.md`, which is identical here and in the site repo; both copies must change together,
plus `fragen.html` in the site repo. Decisions by Sumanth on 2026-11-14:

1. **Parts count:** the case study is right, the corpus is stale. `corpus.md:151`
   "Trainiert auf 1.100 selbst generierten Bauteilen" → 2.272, matching
   `projekte/simready.html:72`.
2. **Positive-control eval case:** expected answer "1.100" → "2.272" in
   `evals/questions.json` (id `positive-control`) and in the site's `fragen.html:162` table row.
3. **Number of test questions:** Sumanth said "fünfzehn" is correct and `fragen.html` must
   change. Conflict to settle first: `evals/questions.json` holds 18 cases and the published
   table in `fragen.html` has 18 rows ("Alle 18 Testfragen", `fragen.html:172`), while
   `automatisierung.html:63` says "fünfzehn". Count again with Sumanth before editing either.
4. **FE programs prepared answer:** `fragen.html:119` says which FE programs he uses "steht
   nicht in diesen Unterlagen". Replace with the tools the CV lists: Simufact Forming, deal.II,
   MATLAB Simscape/Simulink, ParaView (FE/simulation, `profil.html:139`, `corpus.md:29,78`) and
   Siemens NX, PTC Creo, SolidWorks (CAD, `corpus.md:79`). SolidWorks is a CAD tool, not an
   FE program; word the answer so it does not claim otherwise.
5. **SimReady section of corpus.md is older than the case study:** rewrite it from the current
   `projekte/simready.html` (91 % F1 on 3.612 faces, 88/100 image-to-CAD with Qwen2.5-VL-3B
   QLoRA (0/100 before fine-tuning), typed Pydantic DSL, 2.272 graphs split by source part).

After the edits: run the eval (`evals/run_eval.py`), save the result under `evals/results/`,
redeploy the backend on the VPS so the corpus cache refreshes, verify one live answer per
changed fact, and update the eval table in `fragen.html` if any result changed.

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
