"""Put the answer's source line in the language of the question.

The model writes "Quelle:" under English answers (and "Source:" under German ones) in
about three of 21 eval answers despite rule 10. This wraps the event stream: text that
could start a source line is held back until its line ends, then rewritten; all other
text streams through unchanged. When the question's language is unclear, nothing is
rewritten. Each rewrite prints a status line to stderr.
"""
import re
import sys

MARKERS = {"de": "Quelle:", "en": "Source:"}
PHRASES = [  # (German, English) bodies the prompt names, rule 11 and 17
    ("GitHub (live abgefragt)", "GitHub (live queried)"),
    ("keine – steht nicht in den Unterlagen", "none – not in the documents"),
]
DE_WORDS = {"er", "hat", "ist", "war", "was", "wie", "wann", "welche", "welcher", "welchen", "bei",
            "und", "noch", "nicht", "der", "die", "das", "ein", "eine", "mit", "kann", "sein", "seine",
            "gearbeitet", "macht", "gerade", "ab", "für", "oder", "doch", "auf", "zu", "im", "an"}
EN_WORDS = {"he", "did", "does", "is", "was", "what", "how", "when", "which", "the", "at", "has",
            "his", "with", "can", "work", "worked", "still", "now", "doing", "a", "an", "of", "for",
            "or", "in", "on", "to", "him", "any"}
WORD = re.compile(r"[a-zäöüß]+")


def question_language(question):
    """'de', 'en', or None when the words do not tell."""
    text = question.lower()
    words = WORD.findall(text)
    de = sum(w in DE_WORDS for w in words) + 2 * bool(re.search(r"[äöüß]", text))
    en = sum(w in EN_WORDS for w in words)
    if de == en:
        return None
    return "de" if de > en else "en"


def _rewrite(line, lang):
    stripped = line.lstrip()
    lead = line[:len(line) - len(stripped)]
    for marker_lang, marker in MARKERS.items():
        if stripped.startswith(marker) and marker_lang != lang:
            body = stripped[len(marker):]
            for de, en in PHRASES:
                body = body.replace(en, de) if lang == "de" else body.replace(de, en)
            print(f"source line rewritten: {marker} -> {MARKERS[lang]}", file=sys.stderr)
            return lead + MARKERS[lang] + body
    return line


def fix_source_line(events, lang):
    if lang is None:
        yield from events
        return
    held, free = "", False  # held: start of the current line that may still become a source line

    for event in events:
        if event.get("type") != "delta":
            if held:
                yield {"type": "delta", "text": _rewrite(held, lang)}
                held, free = "", False
            yield event
            continue
        out = []
        for ch in event["text"]:
            if ch == "\n":
                out.append(_rewrite(held, lang) + ch)
                held, free = "", False
            elif free:
                out.append(ch)
            else:
                held += ch
                start = held.lstrip()
                if start and not any(m.startswith(start) or start.startswith(m) for m in MARKERS.values()):
                    out.append(held)
                    held, free = "", True
        if out:
            yield {"type": "delta", "text": "".join(out)}
    if held:
        yield {"type": "delta", "text": _rewrite(held, lang)}
