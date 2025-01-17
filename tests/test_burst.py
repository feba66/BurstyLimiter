import time
from burstylimiter import Limiter, BurstyLimiter


@BurstyLimiter(Limiter(1, 1), Limiter(1, 3))
def ratelimited_function():
    return


def test_burst():
    t0 = time.time()
    for _ in range(3):
        ratelimited_function()
    t1 = time.time()
    diff = t1 - t0
    assert diff > 1 and diff < 1.4
