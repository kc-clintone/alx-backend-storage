#/usr/bin/env python3
"""
Class module
"""

from typing import Union
import redis
import uuid


class Cache:
    """
    The class for this module
    """

    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    """
    Stores a value in redis and returns a key
    """
    def store(self, data: Union[str, bytes, int, float]) -> str:
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
