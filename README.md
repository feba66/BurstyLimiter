# BurstyLimiter
This is a library to help with Burst Ratelimits. 
I needed to ratelimit my requests for an API game called [SpaceTradersAPI](https://spacetraders.io/), so i wrote this.
Originally there was a limit of 2 requests per second + 10 requests per ten seconds. 

Small disclaimer: I am now a part of the Team behind SpaceTradersAPI.

## Usage
For the usage look at the code below. ``rate_limited_function`` has a ratelimit of 2/second plus 10 per 10 seconds, just like what i needed for the game.
```sh
pip install burstylimiter
```
```py
from burstylimiter import Limiter, BurstyLimiter

@BurstyLimiter(Limiter(2, 1), Limiter(10, 10))
def rate_limited_function():
    print("I am Ratelimited")
```

## Tests
Each tests needed its own file because pytest messes with the timing if they are not.