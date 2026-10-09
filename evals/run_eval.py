"""Run the grounding eval against the deployed server and write a hand-grading sheet.

    python evals/run_eval.py --url https://api.sumanthreddy.de

Questions run one at a time with a pause, because the server's own per-IP limit
(10 per 10 minutes) applies to this script as well. Auto flags are a pre-screen;
the verdict column is filled in by hand.
"""
import argparse
import json
import re
import sys
import time
from datetime import date
from pathlib import Path

import httpx

HERE = Path(__file__).resolve().parent


def ask(client, url, question, history):
    text, end = "", None
    with client.stream("POST", f"{url}/chat", json={"question": question, "history": history}) as r:
        r.raise_for_status()
        for line in r.iter_lines():
            if not line.strip():
                continue
            event = json.loads(line)
            if event["type"] == "delta":
                text += event["text"]
            else:
                end = event
    return text, end


def auto_flags(case, answer):
    flags = [f"fehlt: /{p}/" for p in case.get("must_match", []) if not re.search(p, answer, re.I)]
    flags += [f"verboten: /{p}/" for p in case.get("must_not_match", []) if re.search(p, answer, re.I)]
    return flags


def md_cell(text):
    return text.strip().replace("|", "\\|").replace("\r\n", "\n").replace("\n", "<br>")


def run_case(client, url, case, pause):
    history = list(case.get("history", []))
    for setup_question in case.get("setup", []):
        text, _ = ask(client, url, setup_question, history)
        history += [{"role": "user", "content": setup_question}, {"role": "assistant", "content": text.strip()}]
        time.sleep(pause)
    return ask(client, url, case["question"], history)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True)
    parser.add_argument("--pause", type=float, default=62.0)
    args = parser.parse_args()
    url = args.url.rstrip("/")
    cases = json.loads((HERE / "questions.json").read_text(encoding="utf-8"))
    rows, models, fallbacks, cache_reads = [], set(), 0, []
    with httpx.Client(timeout=60.0) as client:
        for i, case in enumerate(cases):
            text, end = run_case(client, url, case, args.pause)
            end = end or {"type": "fallback", "reason": "no end event"}
            if end["type"] == "done":
                models.add(end["model"])
                cache_reads.append(end["cache_read"])
                outcome = end["model"]
            else:
                fallbacks += 1
                outcome = f"FALLBACK: {end['reason']}"
            flags = auto_flags(case, text) if end["type"] == "done" else ["kein Modelltext"]
            rows.append(f"| {case['id']} | {md_cell(case['question'])} | {md_cell(case['expect'])} | "
                        f"{md_cell(text)} | {md_cell('; '.join(flags))} | {outcome} |  |")
            print(f"[{i + 1}/{len(cases)}] {case['id']}: {outcome} {flags}", flush=True)
            if case["id"] == "positive-control" and flags:
                print("  POSITIVE CONTROL FAILED – check the harness and corpus before blaming the model")
            if i + 1 < len(cases):
                time.sleep(args.pause)
    label = "-".join(sorted(models)) or "no-model"
    out = HERE / "results" / f"{date.today().isoformat()}-{label}.md"
    header = ["# Eval run", "", f"- URL: {url}", f"- Models seen: {', '.join(sorted(models)) or 'none'}",
              f"- Fallbacks: {fallbacks}", f"- cache_read per call: {cache_reads}", "",
              "| id | Frage | Erwartet | Antwort | Auto-Flags | Ergebnis | Urteil (von Hand) |",
              "|---|---|---|---|---|---|---|"]
    out.write_text("\n".join(header + rows) + "\n", encoding="utf-8")
    print(f"written: {out}")
    return 1 if fallbacks else 0


if __name__ == "__main__":
    sys.exit(main())
