import redis
from django.conf import settings
import hashlib
import pickle

from django.core.exceptions import EmptyResultSet
from django.db.models import QuerySet


class RedisClient:

    @staticmethod
    def get_redis(redis_url=settings.REDIS_URL):
        return redis.Redis.from_url(redis_url)


cache = RedisClient.get_redis()


def cache_serialize_argument(arg):
    if isinstance(arg, QuerySet):
        try:
            return str(arg.query)
        except EmptyResultSet:
            return str(arg)
    else:
        return str(arg)


def cache_get_key(*args, **kwargs) -> str:
    serialise = []
    for arg in args:
        serialise.append(cache_serialize_argument(arg))
    for key, arg in kwargs.items():
        serialise.append(str(key))
        serialise.append(cache_serialize_argument(arg))
    key = hashlib.md5("".join(serialise).encode('utf-8')).hexdigest()
    return key


def cache_for(time):
    def decorator(fn):
        def wrapper(*args, **kwargs):
            key = cache_get_key(fn.__name__, *args, **kwargs)
            result = cache.get(key)
            if result is not None:
                return pickle.loads(result)

            result = fn(*args, **kwargs)
            if result is not None:
                cache.setex(name=key, value=pickle.dumps(result), time=time)
                return result
            else:
                return None

        return wrapper

    return decorator


def get_cached_function_result(time, func, *args, **kwargs):
    @cache_for(time)
    def cached_function(*args, **kwargs):
        return func(*args, **kwargs)

    return cached_function(*args, **kwargs)
