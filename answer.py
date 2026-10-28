"""System prompt, corpus cache and the streamed Anthropic call."""
import json
import sys
import threading
import time
from pathlib import Path

import anthropic
import httpx

from tools import TOOLS, RepoCache, run_tool

HERE = Path(__file__).resolve().parent
SYSTEM_PROMPT = (HERE / "system_prompt.md").read_text(encoding="utf-8").strip()
BOOT_CORPUS = HERE / "corpus.md"
CORPUS_URL = "https://raw.githubusercontent.com/Sumanthreddy-DE/Sumanthreddy-DE.github.io/main/corpus.md"
MAX_TOKENS = 600
MAX_TOOL_ROUNDS = 2


def fetch_text(url):
    response = httpx.get(url, timeout=10.0)
    response.raise_for_status()
    return response.text


def spawn_thread(fn):
    threading.Thread(target=fn, daemon=True).start()


class CorpusCache:
    """The corpus string, re-fetched in the background once the TTL has passed.

    A failed or empty fetch keeps the previous copy; the boot copy shipped with the
    server covers a GitHub outage at start.
    """

    def __init__(self, url=CORPUS_URL, boot_path=BOOT_CORPUS, ttl=3600.0,
                 fetch=fetch_text, clock=time.monotonic, spawn=spawn_thread):
        self.url, self.ttl, self.fetch, self.clock, self.spawn = url, ttl, fetch, clock, spawn
        self._text = Path(boot_path).read_text(encoding="utf-8")
        self._checked = None
        self._refreshing = False
        self._lock = threading.Lock()

    def refresh(self):
        try:
            text = self.fetch(self.url)
            if text.strip():
                self._text = text
        except Exception as exc:  # any fetch failure keeps the old copy
            print(f"corpus refresh failed: {type(exc).__name__}", file=sys.stderr)
        finally:
            self._checked = self.clock()
            self._refreshing = False

    def get(self):
        if self._checked is None or self.clock() - self._checked >= self.ttl:
            with self._lock:
                if not self._refreshing:
                    self._refreshing = True
                    self.spawn(self.refresh)
        return self._text


def build_system(corpus):
    return [{
        "type": "text",
        "text": f"{SYSTEM_PROMPT}\n\n<quellen>\n{corpus}\n</quellen>",
        "cache_control": {"type": "ephemeral"},
    }]


def model_options(model):
    # Sonnet 5 thinks adaptively unless told otherwise. Haiku 4.5 does not think by
    # default and rejects `effort`, so it gets nothing extra. Haiku 5.5 always thinks
    # adaptively and its thinking counts toward max_tokens: low effort, more room.
    options = {"max_tokens": MAX_TOKENS}
    if model.startswith("claude-sonnet-5"):
        options["thinking"] = {"type": "disabled"}
    elif model.startswith("claude-haiku-5-5"):
        options.update(output_config={"effort": "low"}, max_tokens=2000)
    return options


def _fallback(reason, exc=None):
    if exc is not None:
        print(f"anthropic call failed: {type(exc).__name__}", file=sys.stderr)
    return {"type": "fallback", "reason": reason}


def _call(client, model, system, messages, tools, tool_choice):
    """One streamed API call. Yield its deltas and return the final message.

    The generator's return value carries the message out of the `with` block, so the
    caller still sees every delta before it decides what to do next.
    """
    kwargs = dict(model=model, system=system, messages=messages, **model_options(model))
    if tools:
        kwargs["tools"] = tools
    if tool_choice is not None:
        kwargs["tool_choice"] = tool_choice
    with client.messages.stream(**kwargs) as stream:
        for text in stream.text_stream:
            yield {"type": "delta", "text": text}
        return stream.get_final_message()


def _content_blocks(message):
    return [block.model_dump(exclude_none=True) if hasattr(block, "model_dump") else block
            for block in (message.content or [])]


def stream_answer(client, model, system, messages, cache=None):
    """Yield protocol events: zero or more delta|tool, then exactly one done or fallback."""
    cache = cache or RepoCache()
    messages = list(messages)
    rounds = 0
    tool_count = 0
    cache_read = 0
    while True:
        limited = rounds >= MAX_TOOL_ROUNDS
        call = _call(client, model, system, messages, TOOLS,
                     {"type": "none"} if limited else None)
        streamed = False
        try:
            # Not `yield from`: that swallows the generator's StopIteration, and with it
            # the final message the sub-generator returns.
            while True:
                event = next(call)
                streamed = True
                yield event
        except StopIteration as stop:
            final = stop.value
        except anthropic.RateLimitError as exc:
            yield _fallback("upstream_busy", exc)
            return
        except anthropic.APIStatusError as exc:
            yield _fallback("error", exc)
            return
        except anthropic.APIConnectionError as exc:
            yield _fallback("error", exc)
            return
        except Exception as exc:  # anything else mid-stream still ends in a fallback event
            yield _fallback("error", exc)
            return
        finally:
            call.close()

        if final.stop_reason == "end_turn":
            cache_read += final.usage.cache_read_input_tokens or 0
            yield {"type": "done", "model": model, "cache_read": cache_read,
                   "tools": tool_count}
            return
        if final.stop_reason == "max_tokens":
            yield _fallback("truncated")
            return
        if final.stop_reason != "tool_use" or limited:
            yield _fallback("truncated")
            return

        cache_read += final.usage.cache_read_input_tokens or 0
        rounds += 1
        content = _content_blocks(final)
        messages.append({"role": "assistant", "content": content})
        results = []
        for block in content:
            if block.get("type") != "tool_use":
                continue
            tool_count += 1
            result, event = run_tool(block.get("name"), block.get("input"), cache)
            if event is not None:
                yield event
            results.append({"type": "tool_result", "tool_use_id": block["id"],
                            "content": json.dumps(result, ensure_ascii=False)})
        messages.append({"role": "user", "content": results})
        if streamed:
            # Text before a tool call and text after it are two paragraphs; without this
            # the visitor reads "...nach.SimReady wurde...".
            yield {"type": "delta", "text": "\n\n"}
