import time
from burstylimiter.ratelimit import Limiter


@Limiter(1, 1)
def ratelimited_function():
    return


def test_ratelimit():
    t0 = time.time()
    for _ in range(3):
        ratelimited_function()
    t1 = time.time()
    assert t1 - t0 > 2


if __name__ == "__main__":
    test_ratelimit()
