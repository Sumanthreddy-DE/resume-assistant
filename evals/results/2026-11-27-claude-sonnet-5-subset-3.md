# Eval run

Hand-graded 2026-11-27 (rerun-now-currentwork, corpus with the Aktuell line): 3 OK. One false flag on now-en, pattern fixed.

- URL: https://api.sumanthreddy.de
- Models seen: claude-sonnet-5
- Fallbacks: 0
- cache_read per call: [0, 17815, 17815]
- tools per call: [0, 0, 0]

| id | Frage | Erwartet | Antwort | Auto-Flags | Tools | Ergebnis | Urteil (von Hand) |
|---|---|---|---|---|---|---|---|
| now-de | Was macht er gerade? | Lage zuerst: Master 08/2026 abgeschlossen, sucht eine Festanstellung; dazu SimReady und tägliche Deutschpraxis, in eigenen Worten statt CV-Aufzählung; Master und Tutor nie als Gegenwart; kein Tool | Sumanth hat sein Master-Studium abgeschlossen und sucht aktuell eine Festanstellung als Machine Learning Engineer im Engineering-Umfeld. Nebenbei arbeitet er freiberuflich weiter: Sein Buchungs-Bot läuft seit 04/2026 jeden Morgen automatisch, an einem deutschsprachigen KI-Telefonassistenten für lokale Betriebe feilt er gerade, und SimReady, sein KI-Copilot für CAD/FEA-Vorverarbeitung, entwickelt er laufend weiter. Nebenbei übt er täglich 15 Minuten Deutsch.<br><br>Quelle: Lebenslauf |  | - | claude-sonnet-5 | OK: nutzt die Aktuell-Zeile richtig (Bot läuft täglich, Telefonassistent in Arbeit, SimReady als Weiterentwicklung), Zielrolle, Deutschpraxis |
| now-en | What is he doing now? | Situation first: master's finished 08/2026, looking for a full-time job; plus SimReady and daily German practice, in own words, not a CV list; master's and tutoring never as present; no tool | He has finished his master's degree and is currently job-hunting for roles in engineering-focused machine learning, simulation, or mechanical design. Alongside that, he runs a freelance booking bot that emails a caretaker daily, is building a German-language AI phone assistant for local businesses, keeps developing SimReady, and practices German for 15 minutes a day.<br><br>Source: Lebenslauf | fehlt: /(?i)full-time\|job search\|looking for (a )?(job\|position)/ | - | claude-sonnet-5 | OK: alle Punkte inkl. Deutschpraxis; Auto-Flag falsch: "job-hunting" traf das Muster nicht, Muster erweitert |
| start-de | Ab wann kann er anfangen? | Sofort verfügbar; keine erfundene Kündigungsfrist | Er ist sofort verfügbar – sein Master ist abgeschlossen (08/2026), und er sucht aktuell gezielt eine Festanstellung, bevorzugt als Machine Learning Engineer im Engineering-Umfeld.<br><br>Quelle: Lebenslauf |  | - | claude-sonnet-5 | OK |
