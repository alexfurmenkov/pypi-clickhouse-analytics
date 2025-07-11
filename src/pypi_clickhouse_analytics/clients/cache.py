import json
from abc import ABC, abstractmethod
from datetime import timedelta
from typing import Any

from pydantic import BaseModel as PydanticModel

from cachetools import LRUCache
from redis.asyncio import Redis


class CacheClient(ABC):

    @abstractmethod
    async def get(self, key: str, *, default: Any = None) -> Any:
        """
        Gets an item from the cache.
        """

    @abstractmethod
    async def set(self, key: str, value: Any, *, ttl: timedelta | float | None = None) -> Any:
        """
        Gets an item from the cache.
        """

    def _serialize_value(self, value: Any):
        if isinstance(value, PydanticModel):
            return json.dumps(value.model_dump(mode="json"))

        return json.dumps(value)


class RedisCache(CacheClient):
    def __init__(self, redis_client: Redis):
        self.__redis_client = redis_client

    async def get(self, key: str, *, default: Any = None) -> Any:
        item = await self.__redis_client.get(key)

        if item is None:
            return default

        return json.loads(item)

    async def set(self, key: str, value: Any, *, ttl: timedelta | float | None = None) -> Any:
        serialized = self._serialize_value(value)
        await self.__redis_client.set(key, serialized, ex=ttl)


class LocalCache(CacheClient):
    cache: LRUCache = LRUCache(maxsize=100)

    async def get(self, key: str, *, default: Any = None) -> Any:
        return self.cache.get(key, default)

    async def set(self, key: str, value: Any, *, ttl: timedelta | float | None = None) -> Any:
        self.cache[key] = self._serialize_value(value)
