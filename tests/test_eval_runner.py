import json
from pathlib import Path

from evals.run_eval import auto_flags, md_cell

CASES = json.loads((Path(__file__).resolve().parents[1] / "evals" / "questions.json").read_text(encoding="utf-8"))


def case(case_id):
    return next(c for c in CASES if c["id"] == case_id)


def test_fifteen_unique_cases():
    assert len(CASES) == 15
    assert len({c["id"] for c in CASES}) == 15


def test_negated_claim_is_not_flagged_but_a_false_one_is():
    c = case("siemens-de")
    good = "Nein. Er war an der FAU angestellt und nicht bei Siemens angestellt."
    bad = "Nein, aber er war bei Siemens angestellt, sagt die FAU."
    assert auto_flags(c, good) == []
    assert any(f.startswith("verboten") for f in auto_flags(c, bad))


def test_positive_control_flags_a_missing_number():
    assert auto_flags(case("positive-control"), "Etwa tausend Bauteile.") == ["fehlt: /1[.,]?100/"]
    assert auto_flags(case("positive-control"), "1.100 Bauteile.") == []


def test_md_cell_escapes_pipes_and_newlines():
    assert md_cell("a|b\nQuelle: X") == "a\\|b<br>Quelle: X"
