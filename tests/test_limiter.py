import time
from burstylimiter import Limiter


@Limiter(1, 1)
def ratelimited_function():
    return


def test_limiter():
    t0 = time.time()
    for _ in range(3):
        ratelimited_function()
    t1 = time.time()
    diff = t1 - t0
    assert diff > 2 and diff < 2.5
