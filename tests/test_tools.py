from types import SimpleNamespace

from anthropic.types import TextBlock, ToolUseBlock
from anthropic.types.message import Message

import answer
import tools
from tests.test_answer import MSGS, FakeClient, run

SAMPLE = {
    "repo": "simready",
    "description": "Automatisierte Prüfung",
    "stars": 3,
    "pushed_at": "2026-09-14T10:00:00Z",
    "url": "https://github.com/Sumanthreddy-DE/simready",
    "last_commit_sha": "abc1234",
    "last_commit_date": "2026-09-14T10:00:00Z",
    "last_commit_message": "feat: report writer",
}


def fake_fetch(repo):
    if repo == tools.REPOS[0]:
        raise RuntimeError("github down")
    return dict(SAMPLE, repo=repo)


class FakeStream:
    def __init__(self, chunks=(), final=None, exc=None):
        self.chunks, self.exc = list(chunks), exc
        self.final = final or message("end_turn", [TextBlock(type="text", text="Antwort.")])

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
        return self.final


def message(stop, content):
    return Message(id="msg_1", model="claude-haiku-4-5", role="assistant", type="message",
                   stop_reason=stop, stop_sequence=None, content=content,
                   usage={"input_tokens": 10, "output_tokens": 5, "cache_read_input_tokens": 1200})


def tool_use(repo="Peak-Power-Minimization", block_id="tu_1"):
    return ToolUseBlock(type="tool_use", id=block_id, name="get_repo_activity", input={"repo": repo})


def run_script(streams, cache=None):
    client = FakeClient(None)
    opened = list(streams)
    client.messages.stream = lambda **kw: (client.calls.append(kw), opened.pop(0))[1]
    events = list(answer.stream_answer(client, "claude-haiku-4-5", answer.build_system("K"),
                                       MSGS, cache=cache))
    return events, client


def test_tool_round_order_and_count():
    streams = [
        FakeStream(["Ich schaue ", "nach."], message("tool_use", [
            TextBlock(type="text", text="Ich schaue nach."),
            tool_use("Peak-Power-Minimization")])),
        FakeStream(["Es ", "läuft."], message("end_turn", [TextBlock(type="text", text="Es läuft.")])),
    ]
    events, client = run_script(streams, cache=tools.RepoCache(fetch=fake_fetch))

    assert events == [
        {"type": "delta", "text": "Ich schaue "},
        {"type": "delta", "text": "nach."},
        {"type": "tool", "name": "get_repo_activity", "repo": "Peak-Power-Minimization",
         "status": "ok", "summary": "Peak-Power-Minimization · letzter Commit 14.09.2026"},
        {"type": "delta", "text": "\n\n"},
        {"type": "delta", "text": "Es "},
        {"type": "delta", "text": "läuft."},
        {"type": "done", "model": "claude-haiku-4-5", "cache_read": 2400, "tools": 1},
    ]
    assert len(client.calls) == 2
    assert client.calls[0]["tools"] == tools.TOOLS and "tool_choice" not in client.calls[0]
    followup = client.calls[1]["messages"]
    assert followup[-2]["role"] == "assistant"
    assert followup[-2]["content"][1]["type"] == "tool_use"
    assert followup[-1]["role"] == "user"
    assert followup[-1]["content"][0]["tool_use_id"] == "tu_1"
    assert '"last_commit_sha": "abc1234"' in followup[-1]["content"][0]["content"]


def test_unknown_repo_is_rejected_and_nothing_is_fetched():
    calls = []

    def fetch(repo):
        calls.append(repo)
        return SAMPLE

    content, event = tools.run_tool("get_repo_activity", {"repo": "evil/../x"}, tools.RepoCache(fetch=fetch))
    assert content == {"error": "unknown repo"} and event is None and calls == []
    assert tools.run_tool("bash", {"repo": "simready"}, tools.RepoCache(fetch=fetch))[0] == {"error": "unknown repo"}
    assert calls == []


def test_text_after_a_tool_round_is_separated_by_a_blank_line():
    streams = [
        FakeStream(["Ich schaue nach."], message("tool_use", [
            TextBlock(type="text", text="Ich schaue nach."), tool_use("simready")])),
        FakeStream(["Antwort."], message("end_turn", [TextBlock(type="text", text="Antwort.")])),
    ]
    events, _ = run_script(streams, cache=tools.RepoCache(fetch=fake_fetch))

    joined = "".join(e["text"] for e in events if e["type"] == "delta")
    assert joined == "Ich schaue nach.\n\nAntwort."
    assert events[-1]["type"] == "done"


def test_no_separator_when_the_tool_round_streamed_no_text():
    streams = [
        FakeStream([], message("tool_use", [tool_use("Peak-Power-Minimization")])),
        FakeStream(["Antwort."], message("end_turn", [TextBlock(type="text", text="Antwort.")])),
    ]
    events, _ = run_script(streams, cache=tools.RepoCache(fetch=fake_fetch))

    assert "".join(e["text"] for e in events if e["type"] == "delta") == "Antwort."


def test_github_failure_yields_error_event_and_answer_still_finishes():
    streams = [
        FakeStream([], message("tool_use", [tool_use("simready")])),
        FakeStream(["Nicht abrufbar."], message("end_turn", [TextBlock(type="text", text="Nicht abrufbar.")])),
    ]
    events, _ = run_script(streams, cache=tools.RepoCache(fetch=fake_fetch))

    assert events[0] == {"type": "tool", "name": "get_repo_activity", "repo": "simready", "status": "error"}
    assert "summary" not in events[0]
    assert events[-1]["type"] == "done" and events[-1]["tools"] == 1


def test_round_limit_forces_tool_choice_none():
    def tool_round(n):
        return FakeStream([], message("tool_use", [tool_use(block_id=f"tu_{n}")])) 
    streams = [tool_round(1), tool_round(2), FakeStream(["fertig"], message(
        "end_turn", [TextBlock(type="text", text="fertig")]))]
    events, client = run_script(streams, cache=tools.RepoCache(fetch=fake_fetch))

    assert [c.get("tool_choice") for c in client.calls] == [None, None, {"type": "none"}]
    # cache_read sums over all three rounds (1200 each), not just the tool rounds.
    assert events[-1] == {"type": "done", "model": "claude-haiku-4-5", "cache_read": 3600, "tools": 2}


def test_tool_use_after_the_limit_ends_in_fallback_not_done():
    def tool_round(n):
        return FakeStream([], message("tool_use", [tool_use(block_id=f"tu_{n}")]))
    streams = [tool_round(1), tool_round(2), tool_round(3)]
    events, client = run_script(streams, cache=tools.RepoCache(fetch=fake_fetch))
    assert len(client.calls) == 3
    assert events[-1] == {"type": "fallback", "reason": "truncated"}


def test_cache_hit_makes_no_second_fetch():
    calls = []

    def fetch(repo):
        calls.append(repo)
        return dict(SAMPLE, repo=repo)

    cache = tools.RepoCache(fetch=fetch, clock=lambda: 0.0)
    cache.get("simready")
    cache.get("simready")
    assert calls == ["simready"]


def test_cache_expires_after_ttl_and_does_not_store_failures():
    t = {"v": 0.0}
    calls = []

    def fetch(repo):
        calls.append(repo)
        if repo == "simready":
            raise RuntimeError("down")
        return dict(SAMPLE, repo=repo)

    cache = tools.RepoCache(fetch=fetch, clock=lambda: t["v"])
    cache.get("Peak-Power-Minimization")
    t["v"] = 3599
    cache.get("Peak-Power-Minimization")
    t["v"] = 3600
    cache.get("Peak-Power-Minimization")
    assert calls == ["Peak-Power-Minimization"] * 2
    assert tools.run_tool("get_repo_activity", {"repo": "simready"}, cache)[0] == {"error": "unavailable"}
    assert tools.run_tool("get_repo_activity", {"repo": "simready"}, cache)[0] == {"error": "unavailable"}
    assert calls.count("simready") == 2


def test_fetch_repo_builds_both_urls_from_the_allowlist():
    urls = []

    def response(payload):
        return SimpleNamespace(json=lambda: payload, raise_for_status=lambda: None)

    def get(url, **kwargs):
        urls.append((url, kwargs["timeout"]))
        if url.endswith("/commits?per_page=1"):
            return response([{
                "sha": "0123456789abcdef",
                "commit": {"committer": {"date": "2026-01-31T00:00:00Z"}, "message": "fix: x\n\nbody"}}])
        return response({
            "description": None, "stargazers_count": 1, "pushed_at": "2026-01-31T00:00:00Z",
            "html_url": "https://github.com/Sumanthreddy-DE/simready"})

    data = tools.fetch_repo("simready", get=get)
    assert urls == [
        ("https://api.github.com/repos/Sumanthreddy-DE/simready", 5.0),
        ("https://api.github.com/repos/Sumanthreddy-DE/simready/commits?per_page=1", 5.0),
    ]
    assert data["last_commit_sha"] == "0123456"
    assert data["last_commit_message"] == "fix: x"
    assert data["description"] == ""


def test_plain_answer_needs_one_call_and_no_tool_events():
    events, client = run(FakeStream(["Hallo."]))
    assert [e["type"] for e in events] == ["delta", "done"]
    assert events[-1]["tools"] == 0
    assert len(client.calls) == 1
