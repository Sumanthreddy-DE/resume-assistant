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
NAMES = {"CV": "Lebenslauf"}  # wrong source name -> rule-11 name
HINTS = {"de": "(Antworte auf Deutsch.)", "en": "(Answer in English.)"}


def question_language(question):
    """'de', 'en', or None when the words do not tell."""
    text = question.lower()
    words = WORD.findall(text)
    de = sum(w in DE_WORDS for w in words) + 2 * bool(re.search(r"[äöüß]", text))
    en = sum(w in EN_WORDS for w in words)
    if de == en:
        return None
    return "de" if de > en else "en"


def with_language_hint(messages, lang):
    """Append a one-line answer-language hint to the last user turn.

    Rule 10 alone lost against the German system block: "When could he start?" got a
    German answer in the 2026-11-27 full run. The hint sits next to the question, outside
    the cached system block. Unclear language: messages come back unchanged.
    """
    if lang is None:
        return messages
    *head, last = messages
    content = [{"type": "text", "text": last["content"]}, {"type": "text", "text": HINTS[lang]}]
    return [*head, {**last, "content": content}]


def _rename_sources(body):
    """Source names stay German in both languages (rule 11); the model sometimes writes "CV"."""
    out = []
    for name in body.split(","):
        key = name.strip()
        if key in NAMES:
            print(f"source name rewritten: {key} -> {NAMES[key]}", file=sys.stderr)
            name = name.replace(key, NAMES[key])
        out.append(name)
    return ",".join(out)


def _rewrite(line, lang):
    stripped = line.lstrip()
    lead = line[:len(line) - len(stripped)]
    for marker_lang, marker in MARKERS.items():
        if not stripped.startswith(marker):
            continue
        body = _rename_sources(stripped[len(marker):])
        if marker_lang != lang:
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
