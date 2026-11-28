from sourceline import fix_source_line, question_language

DONE = {"type": "done", "model": "m", "cache_read": 0, "tools": 0}


def deltas(*parts):
    return [{"type": "delta", "text": p} for p in parts] + [DONE]


def text(events):
    return "".join(e["text"] for e in events if e["type"] == "delta")


def test_question_language():
    assert question_language("Did he work at Siemens?") == "en"
    assert question_language("What is he doing now?") == "en"
    assert question_language("Hat er bei Siemens gearbeitet?") == "de"
    assert question_language("Ist er noch Tutor an der FAU?") == "de"
    assert question_language("Wie gut ist sein Deutsch?") == "de"
    assert question_language("Und mit welchem Partner?") == "de"
    assert question_language("Hallo") is None


def test_english_answer_with_german_source_line_split_across_deltas():
    # Live 2026-11-26: now-en ended with "Quelle: Lebenslauf, Fallstudie SimReady".
    events = list(fix_source_line(deltas("He is looking for a job.\n\nQu", "elle: Lebenslauf, Fall", "studie SimReady"), "en"))
    assert text(events) == "He is looking for a job.\n\nSource: Lebenslauf, Fallstudie SimReady"
    assert events[-1] == DONE


def test_german_answer_with_english_tool_source_line(capsys):
    # Live 2026-11-26: tool-simready-de ended with "Source: GitHub (live queried)".
    events = list(fix_source_line(deltas("Ja, er arbeitet daran.\n\nSource: GitHub (live queried)"), "de"))
    assert text(events) == "Ja, er arbeitet daran.\n\nQuelle: GitHub (live abgefragt)"
    assert "source line rewritten: Source: -> Quelle:" in capsys.readouterr().err


def test_no_source_phrase_translated_for_english():
    events = fix_source_line(deltas("I cannot help.\n\nQuelle: keine – steht nicht in den Unterlagen"), "en")
    assert text(events) == "I cannot help.\n\nSource: none – not in the documents"


def test_correct_line_untouched_and_body_streams_without_waiting(capsys):
    events = list(fix_source_line(deltas("Nein, ", "Siemens war Partner.", "\n\nQuelle: Lebenslauf"), "de"))
    assert [e["text"] for e in events[:2]] == ["Nein, ", "Siemens war Partner."]
    assert text(events) == "Nein, Siemens war Partner.\n\nQuelle: Lebenslauf"
    assert capsys.readouterr().err == ""


def test_held_text_flushes_before_a_tool_or_fallback_event():
    tool = {"type": "tool", "name": "get_repo_activity"}
    events = list(fix_source_line([{"type": "delta", "text": "So"}, tool, {"type": "delta", "text": "me text"}, DONE], "en"))
    assert events[0] == {"type": "delta", "text": "So"} and events[1] == tool
    assert text(events) == "Some text"


def test_unknown_language_passes_everything_through():
    raw = deltas("Hi.\n\nQuelle: Lebenslauf")
    assert list(fix_source_line(raw, None)) == raw


def test_cv_source_name_becomes_lebenslauf(capsys):
    # Live 2026-11-28: roles-en and start-en ended with "Source: CV" (not a rule-11 name).
    events = list(fix_source_line(deltas("He is available.\n\nSource: C", "V, Fallstudie SimReady"), "en"))
    assert text(events) == "He is available.\n\nSource: Lebenslauf, Fallstudie SimReady"
    assert "CV -> Lebenslauf" in capsys.readouterr().err


def test_cv_in_the_answer_body_is_left_alone():
    events = list(fix_source_line(deltas("His CV lists Python.\n\nSource: Lebenslauf"), "en"))
    assert text(events) == "His CV lists Python.\n\nSource: Lebenslauf"
