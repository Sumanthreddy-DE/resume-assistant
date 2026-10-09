"""Per-IP token bucket and a global daily cap.

State lives in memory, so a restart resets it (accepted, spec §6). Both are called
from the async /chat handler on the event loop, so they need no lock.
"""
import time
from datetime import datetime, timezone


class TokenBucket:
    def __init__(self, capacity=10, per_seconds=600.0, clock=time.monotonic):
        self.capacity = capacity
        self.per_seconds = per_seconds
        self.rate = capacity / per_seconds
        self.clock = clock
        self._state = {}  # key -> (tokens, last_seen)
        self._last_prune = None

    def allow(self, key):
        now = self.clock()
        if self._last_prune is None or now - self._last_prune >= 60:
            self._prune(now)
            self._last_prune = now
        tokens, last = self._state.get(key, (self.capacity, now))
        tokens = min(self.capacity, tokens + (now - last) * self.rate)
        if tokens < 1:
            self._state[key] = (tokens, now)
            return False
        self._state[key] = (tokens - 1, now)
        return True

    def _prune(self, now):
        # A full refill period of inactivity makes an entry equivalent to absent.
        self._state = {k: v for k, v in self._state.items() if now - v[1] < self.per_seconds}


def utc_today():
    return datetime.now(timezone.utc).date()


class DailyCap:
    def __init__(self, cap, today=utc_today):
        self.cap = cap
        self.today = today
        self._day = None
        self._count = 0

    def allow(self):
        day = self.today()
        if day != self._day:
            self._day, self._count = day, 0
        if self._count >= self.cap:
            return False
        self._count += 1
        return True
