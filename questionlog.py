"""Opt-in log of visitor question text, so unanswered recruiter questions become visible.

Off unless LOG_QUESTIONS=true. Stores only the question text (emails and phone numbers
redacted), the UTC date and whether it was a follow-up: no answer, no history, no IP,
no time of day. One JSONL file per day; files older than the retention are deleted.
A write failure never breaks the chat: it prints a status line to stderr instead.
"""
import json
import re
import sys
from datetime import date, timedelta
from pathlib import Path

from limits import utc_today

DEFAULT_DIR = "/var/lib/resume-assistant/questions"
RETENTION_DAYS = 90
EMAIL = re.compile(r"[\w.+-]+@[\w-]+(\.[\w-]+)+")
PHONE = re.compile(r"\+?\d[\d ()/-]{6,}\d")
DAY_FILE = re.compile(r"^(\d{4}-\d{2}-\d{2})\.jsonl$")


def redact(text: str) -> str:
    return PHONE.sub("[phone]", EMAIL.sub("[email]", text))


class QuestionLog:
    def __init__(self, directory=DEFAULT_DIR, retention_days: int = RETENTION_DAYS, today=utc_today):
        self.dir = Path(directory)
        self.retention = timedelta(days=retention_days)
        self.today = today
        self._pruned_on = None

    def record(self, question: str, followup: bool) -> None:
        day = self.today()
        try:
            self.dir.mkdir(parents=True, exist_ok=True)
            if self._pruned_on != day:
                self._prune(day)
                self._pruned_on = day
            line = json.dumps({"date": day.isoformat(), "q": redact(question), "followup": followup},
                              ensure_ascii=False)
            with open(self.dir / f"{day.isoformat()}.jsonl", "a", encoding="utf-8") as f:
                f.write(line + "\n")
        except OSError as exc:
            print(f"question log write failed: {type(exc).__name__}", file=sys.stderr)

    def _prune(self, day: date) -> None:
        cutoff = day - self.retention
        for path in self.dir.iterdir():
            match = DAY_FILE.match(path.name)
            if match and date.fromisoformat(match.group(1)) < cutoff:
                path.unlink()
