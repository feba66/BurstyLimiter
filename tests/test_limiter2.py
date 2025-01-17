import time
from burstylimiter import Limiter


@Limiter(1, 1)
def ratelimited_function():
    return


def test_min_time():
    t0 = time.time()
    for _ in range(1):
        ratelimited_function()
    t1 = time.time()
    diff = t1 - t0
    assert diff < 0.4 and diff > 0
