from datetime import date

from limits import DailyCap, TokenBucket


class Clock:
    def __init__(self):
        self.t = 0.0

    def __call__(self):
        return self.t


def test_bucket_allows_ten_then_blocks():
    b = TokenBucket(clock=Clock())
    assert all(b.allow("1.2.3.4") for _ in range(10))
    assert not b.allow("1.2.3.4")


def test_bucket_is_per_key():
    b = TokenBucket(clock=Clock())
    for _ in range(10):
        b.allow("a")
    assert b.allow("b")


def test_bucket_refills_one_token_per_minute():
    c = Clock()
    b = TokenBucket(clock=c)
    for _ in range(10):
        b.allow("a")
    c.t = 59
    assert not b.allow("a")
    c.t = 61
    assert b.allow("a")


def test_bucket_is_full_again_after_ten_minutes():
    c = Clock()
    b = TokenBucket(clock=c)
    for _ in range(10):
        b.allow("a")
    c.t = 600
    assert all(b.allow("a") for _ in range(10))
    assert not b.allow("a")


def test_stale_entry_pruned_from_state_after_per_seconds_inactivity():
    c = Clock()
    b = TokenBucket(clock=c)
    b.allow("a")
    c.t = 661  # past per_seconds (600) of inactivity and past the 60s prune cadence
    b.allow("other-key")
    assert "a" not in b._state


def test_daily_cap_blocks_then_resets_next_day():
    day = {"v": date(2026, 10, 9)}
    cap = DailyCap(2, today=lambda: day["v"])
    assert cap.allow() and cap.allow()
    assert not cap.allow()
    day["v"] = date(2026, 10, 10)
    assert cap.allow()
