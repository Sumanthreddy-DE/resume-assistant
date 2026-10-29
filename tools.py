"""One read-only tool: live GitHub activity for a fixed allowlist of repositories.

The repo name arrives from the model, so it is never pasted into a URL: the
allowlist enum is the only way in, and the request path is built from a literal
owner plus a value already proven to be one of three known strings.
"""
import sys
import threading
import time

import httpx

OWNER = "Sumanthreddy-DE"
REPOS = ("simready", "PINN-for-composite-interface-identification", "Peak-Power-Minimization")
API = f"https://api.github.com/repos/{OWNER}"
TIMEOUT = 5.0
TTL = 3600.0

TOOL = {
    "name": "get_repo_activity",
    "description": (
        "Live activity of one of Sumanth's public GitHub projects: description, stars, "
        "last push and the latest commit. Use it when a visitor asks whether a project "
        "is active, what changed recently or whether it is still maintained."
    ),
    "input_schema": {
        "type": "object",
        "properties": {"repo": {"type": "string", "enum": list(REPOS)}},
        "required": ["repo"],
    },
}

TOOLS = [TOOL]


class GitHubError(Exception):
    pass


def _get(url, get=httpx.get):
    response = get(url, timeout=TIMEOUT, headers={"Accept": "application/vnd.github+json"})
    response.raise_for_status()
    return response.json()


def fetch_repo(repo, get=httpx.get):
    """Both GitHub calls for one repo, flattened into the fields the model gets."""
    info = _get(f"{API}/{repo}", get=get)
    commits = _get(f"{API}/{repo}/commits?per_page=1", get=get)
    if not isinstance(commits, list) or not commits:
        raise GitHubError("empty commit list")
    commit = commits[0]
    return {
        "repo": repo,
        "description": info.get("description") or "",
        "stars": info.get("stargazers_count", 0),
        "pushed_at": info.get("pushed_at"),
        "url": info.get("html_url"),
        "last_commit_sha": commit["sha"][:7],
        "last_commit_date": commit["commit"]["committer"]["date"],
    }


class RepoCache:
    """Per-repo result, reused for `ttl` seconds. Failures are not cached."""

    def __init__(self, ttl=TTL, fetch=fetch_repo, clock=time.monotonic):
        self.ttl, self.fetch, self.clock = ttl, fetch, clock
        self._entries = {}  # repo -> (fetched_at, data)
        self._lock = threading.Lock()

    def get(self, repo):
        now = self.clock()
        with self._lock:
            hit = self._entries.get(repo)
            if hit and now - hit[0] < self.ttl:
                return hit[1]
        data = self.fetch(repo)
        with self._lock:
            self._entries[repo] = (now, data)
        return data


def _day(iso):
    return f"{iso[8:10]}.{iso[5:7]}.{iso[0:4]}" if iso and len(iso) >= 10 else "?"


def run_tool(name, args, cache):
    """Return (tool_result_content, event). Never raises."""
    args = args if isinstance(args, dict) else {}
    repo = args.get("repo")
    if name != "get_repo_activity" or repo not in REPOS:
        return {"error": "unknown repo"}, None
    try:
        data = cache.get(repo)
        summary = f"{repo} · letzter Commit {_day(data['last_commit_date'])}"
        event = {"type": "tool", "name": name, "repo": repo, "status": "ok", "summary": summary}
        return data, event
    except Exception as exc:  # GitHub down, rate-limited, malformed JSON: all the same to us
        print(f"github lookup failed: {type(exc).__name__}", file=sys.stderr)
        return {"error": "unavailable"}, {"type": "tool", "name": name, "repo": repo, "status": "error"}
