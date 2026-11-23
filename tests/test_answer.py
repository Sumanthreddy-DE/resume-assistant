from datetime import date
from types import SimpleNamespace

import anthropic
import httpx
import httpx2  # anthropic 1.x uses httpx2 objects in its errors

import answer

REQ = httpx2.Request("POST", "https://api.anthropic.com/v1/messages")


class FakeStream:
    def __init__(self, chunks=(), stop="end_turn", cache_read=0, exc=None):
        self.chunks, self.stop, self.cache_read, self.exc = list(chunks), stop, cache_read, exc

    def __enter__(self):
        if self.exc:
            raise self.exc
        return self

    def __exit__(self, *args):
        return False

    @property
    def text_stream(self):
        return iter(self.chunks)

    def get_final_message(self):
        return SimpleNamespace(stop_reason=self.stop,
                               usage=SimpleNamespace(cache_read_input_tokens=self.cache_read))


class FakeClient:
    def __init__(self, stream):
        self.calls = []
        self._stream = stream
        self.messages = SimpleNamespace(stream=self._open)

    def _open(self, **kwargs):
        self.calls.append(kwargs)
        return self._stream


MSGS = [{"role": "user", "content": "Frage"}]


def run(stream, model="claude-haiku-4-5"):
    client = FakeClient(stream)
    return list(answer.stream_answer(client, model, answer.build_system("K"), MSGS)), client


def test_streams_deltas_then_done():
    events, client = run(FakeStream(["Er ", "hat."], cache_read=4200))
    assert events == [{"type": "delta", "text": "Er "}, {"type": "delta", "text": "hat."},
                      {"type": "done", "model": "claude-haiku-4-5", "cache_read": 4200, "tools": 0}]
    assert client.calls[0]["max_tokens"] == 600
    assert client.calls[0]["messages"] == MSGS


def test_max_tokens_stop_ends_in_fallback_not_done():
    events, _ = run(FakeStream(["teil"], stop="max_tokens"))
    assert events[-1] == {"type": "fallback", "reason": "truncated"}


def test_rate_limit_error_becomes_upstream_busy():
    exc = anthropic.RateLimitError("busy", response=httpx2.Response(429, request=REQ), body=None)
    events, _ = run(FakeStream(exc=exc))
    assert events == [{"type": "fallback", "reason": "upstream_busy"}]


def test_server_and_connection_errors_become_error():
    exc = anthropic.InternalServerError("boom", response=httpx2.Response(500, request=REQ), body=None)
    assert run(FakeStream(exc=exc))[0] == [{"type": "fallback", "reason": "error"}]
    assert run(FakeStream(exc=anthropic.APIConnectionError(request=REQ)))[0] == [
        {"type": "fallback", "reason": "error"}]


def test_unexpected_exception_mid_stream_becomes_error_fallback():
    events, _ = run(FakeStream(exc=ValueError("x")))
    assert events == [{"type": "fallback", "reason": "error"}]


def test_model_options_per_model():
    _, haiku = run(FakeStream(["x"]), model="claude-haiku-4-5")
    _, sonnet = run(FakeStream(["x"]), model="claude-sonnet-5")
    assert "thinking" not in haiku.calls[0] and "output_config" not in haiku.calls[0]
    assert sonnet.calls[0]["thinking"] == {"type": "disabled"}
    assert haiku.calls[0]["max_tokens"] == 600


def test_haiku_5_5_thinks_at_low_effort_with_room_for_thinking():
    # Haiku 5.5 thinks adaptively by default and its thinking counts toward max_tokens,
    # so it gets low effort and a larger ceiling instead of a disabled thinking switch.
    _, client = run(FakeStream(["x"]), model="claude-haiku-5-5")
    call = client.calls[0]
    assert call["output_config"] == {"effort": "low"}
    assert call["max_tokens"] == 2000
    assert "thinking" not in call


def test_system_block_is_cached_and_holds_corpus():
    system = answer.build_system("KORPUS-TEXT", today=date(2026, 11, 23))
    assert system[0]["cache_control"] == {"type": "ephemeral"}
    assert "<quellen>\nKORPUS-TEXT\n</quellen>" in system[0]["text"]
    assert "Quelle:" in system[0]["text"] and "dritten Person" in system[0]["text"]


def test_today_sits_in_an_uncached_block_after_the_corpus():
    system = answer.build_system("K", today=date(2026, 11, 23))
    assert len(system) == 2
    assert "cache_control" not in system[1]
    assert system[1]["text"] == "<heute>23.11.2026 (11/2026)</heute>"
    assert "23.11.2026" not in system[0]["text"]  # the date never breaks the cached prefix


def test_today_defaults_to_the_current_utc_date(monkeypatch):
    monkeypatch.setattr(answer, "utc_today", lambda: date(2027, 1, 5))
    assert answer.build_system("K")[1]["text"] == "<heute>05.01.2027 (01/2027)</heute>"


def make_cache(tmp_path, fetch, clock=lambda: 0.0):
    boot = tmp_path / "corpus.md"
    boot.write_text("BOOT", encoding="utf-8")
    return answer.CorpusCache(url="u", boot_path=boot, ttl=3600, fetch=fetch, clock=clock,
                              spawn=lambda fn: fn())


def test_cache_serves_boot_copy_when_fetch_fails(tmp_path):
    def fail(url):
        raise httpx.ConnectError("down")
    assert make_cache(tmp_path, fail).get() == "BOOT"


def test_cache_refreshes_when_stale_and_ignores_empty(tmp_path):
    t = {"v": 0.0}
    texts = iter(["NEU", "   "])
    cache = make_cache(tmp_path, lambda url: next(texts), clock=lambda: t["v"])
    cache.get()                 # first call: stale, fetches "NEU" synchronously via spawn
    assert cache.get() == "NEU"
    t["v"] = 3600
    cache.get()                 # stale again: fetch returns blank, old text kept
    assert cache.get() == "NEU"


def test_periods_are_marked_finished_or_running_against_today():
    corpus = ("#### Tutor (09/2025 – 08/2026, Erlangen)\n"
              "#### SimReady (03/2026 – heute, Projekt)\n"
              "#### Rolle (10/2026 – 12/2026)\n"
              "- Zeitraum: 10/2025 – 02/2026\n"
              "- Zeitraum: seit 03/2026\n"
              "Bereich 2020 – 2022 ohne Monat bleibt.")
    out = answer.annotate_periods(corpus, date(2026, 11, 23))
    assert "(09/2025 – 08/2026 · abgeschlossen, Erlangen)" in out
    assert "(03/2026 – heute · laufend, Projekt)" in out
    assert "(10/2026 – 12/2026 · laufend)" in out
    assert "Zeitraum: 10/2025 – 02/2026 · abgeschlossen\n" in out
    assert "seit 03/2026 · laufend" in out
    assert "2020 – 2022 ohne Monat bleibt." in out


def test_a_period_ending_this_month_is_still_running():
    assert answer.annotate_periods("(09/2025 – 11/2026)", date(2026, 11, 23)) == "(09/2025 – 11/2026 · laufend)"
    assert answer.annotate_periods("(09/2025 – 10/2026)", date(2026, 11, 1)) == "(09/2025 – 10/2026 · abgeschlossen)"


def test_build_system_annotates_the_cached_corpus():
    system = answer.build_system("Tutor (09/2025 – 08/2026)", today=date(2026, 11, 23))
    assert "Tutor (09/2025 – 08/2026 · abgeschlossen)" in system[0]["text"]
