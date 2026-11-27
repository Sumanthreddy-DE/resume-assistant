# Eval run

Hand-graded 2026-11-27 (second sample for rerun-now-currentwork, run 19:46 after the corpus TTL): 2 OK, 1 partial. All three use the Aktuell line correctly; now-en dropped daily German practice (present in the 19:06 sample, subset-3).

- URL: https://api.sumanthreddy.de
- Models seen: claude-sonnet-5
- Fallbacks: 0
- cache_read per call: [17815, 17815, 17815]
- tools per call: [0, 0, 0]

| id | Frage | Erwartet | Antwort | Auto-Flags | Tools | Ergebnis | Urteil (von Hand) |
|---|---|---|---|---|---|---|---|
| now-de | Was macht er gerade? | Lage zuerst: Master 08/2026 abgeschlossen, sucht eine Festanstellung; dazu SimReady und tägliche Deutschpraxis, in eigenen Worten statt CV-Aufzählung; Master und Tutor nie als Gegenwart; kein Tool | Er hat sein Masterstudium abgeschlossen und sucht derzeit eine Festanstellung. Nebenbei übt er täglich 15 Minuten Deutsch im Gespräch mit einer KI. Freiberuflich betreibt er seit 04/2026 einen Buchungs-Bot, der morgens automatisch Küchenbuchungen per E-Mail verschickt, entwickelt einen deutschsprachigen KI-Telefonassistenten für lokale Betriebe und arbeitet weiter an SimReady, seinem CAD-Prüf- und Simulationswerkzeug.<br><br>Quelle: Lebenslauf |  | - | claude-sonnet-5 | OK: Aktuell-Zeile richtig (Bot läuft seit 04/2026 jeden Morgen, Telefonassistent in Entwicklung, SimReady als Weiterarbeit, nicht als Tagesgeschäft); Deutschpraxis, Master als Vergangenheit |
| now-en | What is he doing now? | Situation first: master's finished 08/2026, looking for a full-time job; plus SimReady and daily German practice, in own words, not a CV list; master's and tutoring never as present; no tool | He has finished his Master's degree and is currently looking for a full-time position. Alongside that search, he works freelance: a booking bot that has run automatically every morning since 04/2026, an AI phone assistant for local businesses still in development, and ongoing work on SimReady, his tool that checks and heals CAD geometry for simulation with an LLM agent.<br><br>Source: Lebenslauf | fehlt: /(?i)(practi[sc]\w*\|speak\w*\|train\w*)[^.\n]{0,60}German\|German[^.\n]{0,60}(practi[sc]\|conversation\|every day\|daily)/ | - | claude-sonnet-5 | PARTIAL: current work right (bot every morning since 04/2026, phone assistant still in development, SimReady as ongoing work, not daily work), but daily German practice missing; flag is real |
| start-de | Ab wann kann er anfangen? | Sofort verfügbar; keine erfundene Kündigungsfrist | Er ist laut seinem Profil sofort verfügbar – sein Master wurde bereits im 08/2026 abgeschlossen, und er sucht derzeit aktiv eine Festanstellung. Nebenbei arbeitet er an einem Buchungs-Bot und einem KI-Telefonassistenten sowie an SimReady weiter.<br><br>Quelle: Lebenslauf |  | - | claude-sonnet-5 | OK: sofort verfügbar, keine Kündigungsfrist; Nebensatz zur aktuellen Arbeit korrekt, aber nicht gefragt; "im 08/2026" kleiner Grammatikfehler |
