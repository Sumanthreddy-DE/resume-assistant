"""Measure the cached system prefix against each candidate model's minimum.

    ANTHROPIC_API_KEY=… python count_prompt_tokens.py

count_tokens is free. Below the minimum, cache_control is silently ignored.
"""
import anthropic

from answer import CorpusCache, build_system

MINIMUM = {"claude-haiku-4-5": 4096, "claude-sonnet-5": 1024}


def main():
    corpus = CorpusCache()
    corpus.refresh()
    client = anthropic.Anthropic()
    for model, minimum in MINIMUM.items():
        n = client.messages.count_tokens(model=model, system=build_system(corpus.get()),
                                         messages=[{"role": "user", "content": "Test"}]).input_tokens
        verdict = "OK, will cache" if n >= minimum else "BELOW minimum, will not cache"
        print(f"{model}: {n} input tokens (minimum {minimum}) – {verdict}")


if __name__ == "__main__":
    main()
