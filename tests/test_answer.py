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
                      {"type": "done", "model": "claude-haiku-4-5", "cache_read": 4200}]
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


def test_model_options_per_model():
    _, haiku = run(FakeStream(["x"]), model="claude-haiku-4-5")
    _, sonnet = run(FakeStream(["x"]), model="claude-sonnet-5")
    assert "thinking" not in haiku.calls[0] and "output_config" not in haiku.calls[0]
    assert sonnet.calls[0]["thinking"] == {"type": "disabled"}


def test_system_block_is_cached_and_holds_corpus():
    system = answer.build_system("KORPUS-TEXT")
    assert len(system) == 1
    assert system[0]["cache_control"] == {"type": "ephemeral"}
    assert "<quellen>\nKORPUS-TEXT\n</quellen>" in system[0]["text"]
    assert "Quelle:" in system[0]["text"] and "dritten Person" in system[0]["text"]


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
