#/usr/bin/env python3
"""
Cache class module: Writing strings to Redis
"""

from typing import Union
import redis
import uuid


class Cache:
    """
    This class writes data to a redis instance
    """

    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Stores a value in redis and returns a key
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
