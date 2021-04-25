import functools
import time


def retry(max=3, time_sleep=2):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attemp = 0
            while attemp < max:
                try:
                    return func(*args, **kwargs)
                except:
                    attemp += 1
                    time.sleep(1)
        return wrapper
    return decorator
