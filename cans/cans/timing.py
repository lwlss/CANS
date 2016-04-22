"""Functions for timing code."""

import time

def timeme(method):
    # http://stackoverflow.com/questions/889900/accurate-timing-of-functions-in-python
    def wrapper(*args, **kw):
        startTime = int(round(time.time() * 1000))
        result = method(*args, **kw)
        endTime = int(round(time.time() * 1000))
        print(endTime - startTime,'ms')
        return result
    return wrapper
