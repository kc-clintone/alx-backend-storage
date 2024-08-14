#!/usr/bin/env python3
"""A module for using the Redis NoSQL data storage."""

from functools import wraps
from typing import Any, Callable, Union
import redis
import uuid


def count_calls(method: Callable) -> Callable:
    """
    Decorator that tracks the number of times a method is called
    within the Cache class. The call count is stored in Redis
    using the method's qualified name as the key.
    """

    @wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        """
        Wrapper function that increments the call counter
        before invoking the original method.
        """
        if isinstance(self._redis, redis.Redis):
            self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)

    return wrapper


def track_call_history(method: Callable) -> Callable:
    """
    Decorator that tracks the call history (arguments and results)
    of a method within the Cache class. The input arguments and
    outputs are stored in Redis lists.
    """

    @wraps(method)
    def wrapper_with_history(self, *method_args, **method_kwargs) -> Any:
        """
        Wrapper function that stores the method's input arguments
        and output in Redis, then returns the method's output.
        """
        input_list_key = f"{method.__qualname__}:inputs"
        output_list_key = f"{method.__qualname__}:outputs"

        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(input_list_key, str(method_args))

        result = method(self, *method_args, **method_kwargs)

        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(output_list_key, result)

        return result

    return wrapper_with_history


def replay_call_history(fn: Callable) -> None:
    """
    Displays the call history of a method in the Cache class.
    The history includes the number of calls, input arguments,
    and outputs for each invocation.
    """
    if fn is None or not hasattr(fn, "__self__"):
        return

    redis_instance = getattr(fn.__self__, "_redis", None)

    if not isinstance(redis_instance, redis.Redis):
        return

    method_name = fn.__qualname__
    input_list_key = f"{method_name}:inputs"
    output_list_key = f"{method_name}:outputs"

    call_count = 0

    if redis_instance.exists(method_name) != 0:
        call_count = int(redis_instance.get(method_name))

    print(f"{method_name} was called {call_count} times:")

    input_history = redis_instance.lrange(input_list_key, 0, -1)
    output_history = redis_instance.lrange(output_list_key, 0, -1)

    for method_input, method_output in zip(input_history, output_history):
        print(f"{method_name}(*{method_input.decode('utf-8')}) -> {method_output}")


class Cache:
    """Represents an object for storing data in a Redis data storage."""

    def __init__(self) -> None:
        """
        Initializes the Cache instance by creating a connection
        to the Redis server and flushing the database.
        """
        self._redis = redis.Redis()
        self._redis.flushdb(True)

    @track_call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Stores a value in the Redis data storage and returns a unique key.
        The key is generated using UUID.
        """
        data_key = str(uuid.uuid4())
        self._redis.set(data_key, data)
        return data_key

    def get(
            self,
            key: str,
            fn: Callable = None,
            ) -> Union[str, bytes, int, float]:
        """
        Retrieves a value from the Redis data storage by key.
        If a callable 'fn' is provided, the retrieved data is
        passed through 'fn' before being returned.
        """
        data = self._redis.get(key)
        return fn(data) if fn is not None else data

    def get_str(self, key: str) -> str:
        """
        Retrieves a string value from the Redis data storage by key.
        The data is decoded from bytes to a UTF-8 string.
        """
        return self.get(key, lambda x: x.decode('utf-8'))

    def get_int(self, key: str) -> int:
        """
        Retrieves an integer value from the Redis data storage by key.
        The data is converted from bytes to an integer.
        """
        return self.get(key, lambda x: int(x))
