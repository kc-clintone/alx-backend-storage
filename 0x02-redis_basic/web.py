#!/usr/bin/env python3
"""
Module for fetching and caching web pages.
"""


from functools import wraps
import redis
import requests
from typing import Callable


redis_client = redis.Redis()

def count_accesses_and_cache(expiration: int = 10) -> Callable:
    """
    Decorator to count URL accesses and cache the result.
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(url: str, *args, **kwargs) -> str:
            redis_client.incr(f"count:{url}")

            cached_content = redis_client.get(url)
            if cached_content:
                return cached_content.decode('utf-8')

            content = func(url, *args, **kwargs)

            redis_client.setex(url, expiration, content)
            return content

        return wrapper
    return decorator

@count_accesses_and_cache(expiration=10)
def get_page(url: str) -> str:
    """
    Retrieves the HTML content of a given URL and returns it.
    """
    response = requests.get(url)
    return response.text
