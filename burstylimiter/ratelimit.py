from datetime import datetime, timedelta, timezone
from functools import wraps
from threading import Lock, Semaphore
import time
from typing import Any

TIME_SLEEP_FACTOR = 0.98


class Limiter:
    points: int
    duration: float
    sema: Semaphore
    time: datetime | None
    lock: Lock

    def __init__(self, points: int = 2, duration: float = 1) -> None:
        self.points = points
        self.duration = duration
        self.sema = Semaphore(points)
        self.time = None
        self.lock = Lock()

    def check_reset(self):
        with self.lock:
            if (
                self.time is not None
                and (datetime.now(timezone.utc) - self.time).total_seconds() > 0
            ):
                self.sema._value = self.points
                self.time = None
                return True
        return False

    def aquire(self):
        with self.lock:
            if self.time is None:
                self.time = datetime.now(timezone.utc)
                self.time += timedelta(seconds=self.duration)
        return self.sema.acquire(blocking=False)

    def time_to_reset(self):
        return (
            (self.time - datetime.now(timezone.utc)).total_seconds()
            if self.time is not None
            else 0
        )

    def sleep(self):
        time.sleep(
            max((self.duration - self.time_to_reset()) * TIME_SLEEP_FACTOR, 0.01)
        )

    def __call__(self, func) -> Any:
        @wraps(func)
        def wrapper(*args, **kwargs):
            self.check_reset()

            while not self.aquire():
                if not self.check_reset():
                    self.sleep()

            r = func(*args, **kwargs)
            return r

        return wrapper


class BurstyLimiter:
    static: Limiter
    burst: Limiter

    def __init__(self, static: Limiter, burst: Limiter) -> None:
        self.static = static
        self.burst = burst

    def __call__(self, func) -> Any:
        @wraps(func)
        def wrapper(*args, **kwargs):
            self.static.check_reset()
            self.burst.check_reset()

            while (not self.static.aquire()) and (not self.burst.aquire()):
                if not self.static.check_reset() and not self.burst.check_reset():
                    time.sleep(
                        max(
                            min(self.static.time_to_reset(), self.burst.time_to_reset())
                            * TIME_SLEEP_FACTOR,
                            0,
                        )
                    )

            return func(*args, **kwargs)

        return wrapper
