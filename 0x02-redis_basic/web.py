#!/usr/bin/env python3
"""
Module for fetching and caching web pages.
"""


from functools import wraps
import redis
import requests
from typing import Callable


cache = redis.Redis()


def cache_page(expiration: int = 10) -> Callable:
    """
    Decorator to cache the HTML content of a URL with a specified
    expiration time.
    """

    def decorator(func: Callable) -> Callable:
    """
    Caches output
    """
        @wraps(func)
        def wrapper(url: str) -> str:
            cache_key = f"count:{url}"

            cached_content = cache.get(cache_key)
            if cached_content:
                return cached_content.decode('utf-8')

            content = func(url)
            cache.setex(cache_key, expiration, content)

            return content

        return wrapper

    return decorator


@cache_page(10)
def get_page(url: str) -> str:
    """
    Fetches the HTML content of a given URL and tracks access count.
    The result is cached with an expiration time.
    """

    cache.incr(f"count:{url}")

    response = requests.get(url)
    return response.text
