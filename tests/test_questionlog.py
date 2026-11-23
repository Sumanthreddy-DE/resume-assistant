import json
from datetime import date

from questionlog import QuestionLog, redact


def read(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def test_record_writes_question_text_date_and_followup_only(tmp_path):
    log = QuestionLog(tmp_path, today=lambda: date(2026, 11, 23))
    log.record("Was macht er gerade?", followup=False)
    log.record("Und danach?", followup=True)
    assert read(tmp_path / "2026-11-23.jsonl") == [
        {"date": "2026-11-23", "q": "Was macht er gerade?", "followup": False},
        {"date": "2026-11-23", "q": "Und danach?", "followup": True},
    ]


def test_emails_and_phone_numbers_are_redacted():
    assert redact("Mail an max.muster@firma.de bitte") == "Mail an [email] bitte"
    assert redact("Ruf mich an: +49 176 1234 5678.") == "Ruf mich an: [phone]."
    assert redact("Was hat er 2020 bis 2022 gemacht?") == "Was hat er 2020 bis 2022 gemacht?"


def test_files_older_than_retention_are_deleted_once_a_day(tmp_path):
    for name in ("2026-08-24.jsonl", "2026-08-25.jsonl", "notes.txt"):
        (tmp_path / name).write_text("{}\n", encoding="utf-8")
    log = QuestionLog(tmp_path, retention_days=90, today=lambda: date(2026, 11, 23))
    log.record("Frage?", followup=False)
    assert sorted(p.name for p in tmp_path.iterdir()) == ["2026-08-25.jsonl", "2026-11-23.jsonl", "notes.txt"]


def test_a_write_failure_never_raises_and_says_why(tmp_path, capsys):
    blocker = tmp_path / "file"
    blocker.write_text("x", encoding="utf-8")
    log = QuestionLog(blocker / "sub", today=lambda: date(2026, 11, 23))
    log.record("Frage?", followup=False)
    assert "question log write failed" in capsys.readouterr().err
