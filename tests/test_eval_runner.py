import json
from pathlib import Path

import httpx

from evals import run_eval
from evals.run_eval import auto_flags, md_cell

CASES = json.loads((Path(__file__).resolve().parents[1] / "evals" / "questions.json").read_text(encoding="utf-8"))


def case(case_id):
    return next(c for c in CASES if c["id"] == case_id)


def test_nineteen_unique_cases():
    assert len(CASES) == 19
    assert len({c["id"] for c in CASES}) == 19


def test_negated_claim_is_not_flagged_but_a_false_one_is():
    c = case("siemens-de")
    good = "Nein. Siemens war Kooperationspartner, er war dort nicht angestellt."
    bad = "Nein, aber er war bei Siemens angestellt, sagt die FAU."
    assert auto_flags(c, good) == []
    assert any(f.startswith("verboten") for f in auto_flags(c, bad))


def test_positive_control_flags_a_missing_number():
    assert auto_flags(case("positive-control"), "Etwa tausend Bauteile.") == ["fehlt: /1[.,]?100/"]
    assert auto_flags(case("positive-control"), "1.100 Bauteile.") == []


def test_md_cell_escapes_pipes_and_newlines():
    assert md_cell("a|b\nQuelle: X") == "a\\|b<br>Quelle: X"


def test_siemens_en_negations_are_not_flagged():
    c = case("siemens-en")
    for good in ("No, he never worked for Siemens; Siemens was a cooperation partner.",
                 "No. Siemens was a partner, not his employer."):
        assert auto_flags(c, good) == [], good


def test_frontend_hedge_is_not_flagged_but_verdict_is():
    c = case("frontend")
    hedge = "Frontend-Arbeit ist nicht dokumentiert; es liegt keine Erfahrung in den Quellen vor."
    verdict = "Frontend steht nicht in den Quellen, er hat keine Erfahrung damit."
    assert auto_flags(c, hedge) == []
    assert any(f.startswith("verboten") for f in auto_flags(c, verdict))


def test_phd_wrong_yes_is_flagged():
    c = case("phd")
    assert auto_flags(c, "Nein, er hat nicht promoviert.") == []
    assert auto_flags(c, "Ja, er hat promoviert, aber nicht an der TU.") != []


def test_python_years_singular_is_flagged():
    assert auto_flags(case("python-years"), "Das steht nicht da, etwa 1 Jahr.") != []


def test_a_network_error_on_one_case_does_not_lose_the_run(monkeypatch):
    def broken(*args, **kwargs):
        raise httpx.ConnectError("getaddrinfo failed")
    monkeypatch.setattr(run_eval, "run_case", broken)
    text, end, tools = run_eval.run_case_safely(None, "u", case("phd"), 0)
    assert text == "" and end == {"type": "fallback", "reason": "harness: ConnectError"} and tools == []


def test_expect_tool_flags_in_both_directions():
    tool_case = case("tool-simready-de")
    good_answer = "Der letzte Commit war am 14.09.2026.\n\nQuelle: GitHub (live abgefragt)"
    tool_event = {"type": "tool", "name": "get_repo_activity", "repo": "simready", "status": "ok"}
    assert "Tool erwartet, nicht aufgerufen" in auto_flags(tool_case, good_answer, [])
    assert auto_flags(tool_case, good_answer, [tool_event]) == []

    no_tool_case = case("siemens-de")
    good_siemens = "Nein, Siemens war ein Projektpartner in Kooperation, nicht sein Arbeitgeber."
    assert auto_flags(no_tool_case, good_siemens, []) == []
    assert auto_flags(no_tool_case, good_siemens, [tool_event]) == [
        "Tool unerwartet aufgerufen: simready"
    ]


def test_relative_time_flagged_when_tool_fired():
    tool_case = case("tool-simready-de")
    tool_event = {"type": "tool", "name": "get_repo_activity", "repo": "simready", "status": "ok"}
    for bad in (
        "Der letzte Commit war vor 3 Tagen (2026).\n\nQuelle: GitHub",
        "Das Projekt läuft noch (2026).\n\nQuelle: GitHub",
        "Last commit 2 weeks ago in 2026.\n\nSource: GitHub",
    ):
        assert "relative Zeitangabe" in auto_flags(tool_case, bad, [tool_event]), bad
    clean = "Der letzte Commit war am 14.09.2026.\n\nQuelle: GitHub (live abgefragt)"
    assert "relative Zeitangabe" not in auto_flags(tool_case, clean, [tool_event])


def test_tool_event_is_collected_and_does_not_overwrite_end():
    class FakeResponse:
        def __init__(self, lines):
            self._lines = lines

        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

        def raise_for_status(self):
            pass

        def iter_lines(self):
            return iter(self._lines)

    class FakeHttpClient:
        def __init__(self, lines):
            self._lines = lines

        def stream(self, method, url, json):
            return FakeResponse(self._lines)

    tool_evt = {"type": "tool", "name": "get_repo_activity", "repo": "simready", "status": "ok"}
    done_evt = {"type": "done", "model": "claude-sonnet-5", "cache_read": 7726, "tools": 1}
    lines = [
        json.dumps({"type": "delta", "text": "Vorab."}),
        json.dumps(tool_evt),
        json.dumps({"type": "delta", "text": "\n\nNachher."}),
        json.dumps(done_evt),
    ]
    text, end, tools = run_eval.ask(FakeHttpClient(lines), "http://127.0.0.1:8100", "Frage?", [])
    assert text == "Vorab.\n\nNachher."
    assert end == done_evt
    assert tools == [tool_evt]

    # If the stream ends right after a tool event without done/fallback, end stays None.
    _, end_unfinished, tools_unfinished = run_eval.ask(
        FakeHttpClient(lines[:2]), "http://127.0.0.1:8100", "Frage?", []
    )
    assert end_unfinished is None
    assert tools_unfinished == [tool_evt]


def test_german_negations_are_not_flagged():
    c = case("siemens-de")
    for good in ("Nein, er war nie bei Siemens angestellt, nur Kooperation.",
                 "Nein, er war niemals bei Siemens beschäftigt; Siemens war Kooperationspartner.",
                 "Nein, er hatte keine Anstellung bei Siemens, nur die Kooperation.",
                 "Nein, kein Arbeitsverhältnis mit Siemens, nur Kooperation."):
        assert auto_flags(c, good) == [], good


def test_bmw_negations_are_not_flagged():
    c = case("bmw")
    assert auto_flags(c, "Nein, er hat nie bei BMW gearbeitet.") == []
    assert auto_flags(c, "Nein, bei BMW war er nie angestellt.") == []
