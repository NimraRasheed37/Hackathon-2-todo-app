"""Cache service using Dapr state store for caching."""
import json
from typing import Optional, Any
import os

from src.events.dapr_client import get_dapr_client
from src.core.logging_config import get_logger

logger = get_logger(__name__)

# Check if caching is enabled
CACHE_ENABLED = os.getenv("CACHE_ENABLED", "true").lower() == "true"
DEFAULT_TTL = int(os.getenv("CACHE_TTL_SECONDS", "300"))  # 5 minutes default


class CacheService:
    """Service for caching data using Dapr state store."""

    def __init__(self, store_name: str = "statestore"):
        self.store_name = store_name
        self.client = get_dapr_client() if CACHE_ENABLED else None

    async def get(self, key: str) -> Optional[Any]:
        """Get a value from the cache.

        Args:
            key: Cache key

        Returns:
            Cached value or None if not found
        """
        if not CACHE_ENABLED or not self.client:
            return None

        try:
            value = await self.client.get_state(key)
            if value:
                logger.debug(f"Cache hit: {key}")
                return value
            logger.debug(f"Cache miss: {key}")
            return None
        except Exception as e:
            logger.warning(f"Cache get error for {key}: {e}")
            return None

    async def set(
        self,
        key: str,
        value: Any,
        ttl_seconds: Optional[int] = None
    ) -> bool:
        """Set a value in the cache.

        Args:
            key: Cache key
            value: Value to cache (must be JSON serializable)
            ttl_seconds: Time to live in seconds (defaults to DEFAULT_TTL)

        Returns:
            True if successful
        """
        if not CACHE_ENABLED or not self.client:
            return False

        if ttl_seconds is None:
            ttl_seconds = DEFAULT_TTL

        try:
            await self.client.save_state(key, value, ttl_seconds)
            logger.debug(f"Cache set: {key} (TTL: {ttl_seconds}s)")
            return True
        except Exception as e:
            logger.warning(f"Cache set error for {key}: {e}")
            return False

    async def delete(self, key: str) -> bool:
        """Delete a value from the cache.

        Args:
            key: Cache key

        Returns:
            True if successful
        """
        if not CACHE_ENABLED or not self.client:
            return False

        try:
            await self.client.delete_state(key)
            logger.debug(f"Cache delete: {key}")
            return True
        except Exception as e:
            logger.warning(f"Cache delete error for {key}: {e}")
            return False

    async def get_or_set(
        self,
        key: str,
        factory,
        ttl_seconds: Optional[int] = None
    ) -> Any:
        """Get a value from cache, or compute and cache it.

        Args:
            key: Cache key
            factory: Async function to compute the value if not cached
            ttl_seconds: Time to live in seconds

        Returns:
            The cached or computed value
        """
        # Try to get from cache
        value = await self.get(key)
        if value is not None:
            return value

        # Compute the value
        if asyncio.iscoroutinefunction(factory):
            value = await factory()
        else:
            value = factory()

        # Cache it
        await self.set(key, value, ttl_seconds)
        return value

    def make_key(self, *parts: str) -> str:
        """Create a cache key from parts.

        Args:
            *parts: Key components

        Returns:
            Formatted cache key
        """
        return ":".join(str(p) for p in parts)


# Helper functions for common cache patterns

async def cache_user_tasks(user_id: str, tasks: list) -> bool:
    """Cache a user's task list."""
    cache = CacheService()
    key = cache.make_key("user", user_id, "tasks")
    return await cache.set(key, tasks, ttl_seconds=60)  # 1 minute TTL


async def get_cached_user_tasks(user_id: str) -> Optional[list]:
    """Get cached user tasks."""
    cache = CacheService()
    key = cache.make_key("user", user_id, "tasks")
    return await cache.get(key)


async def invalidate_user_tasks(user_id: str) -> bool:
    """Invalidate user task cache."""
    cache = CacheService()
    key = cache.make_key("user", user_id, "tasks")
    return await cache.delete(key)


async def cache_task(task_id: int, task_data: dict) -> bool:
    """Cache a single task."""
    cache = CacheService()
    key = cache.make_key("task", str(task_id))
    return await cache.set(key, task_data, ttl_seconds=300)


async def get_cached_task(task_id: int) -> Optional[dict]:
    """Get a cached task."""
    cache = CacheService()
    key = cache.make_key("task", str(task_id))
    return await cache.get(key)


async def invalidate_task(task_id: int) -> bool:
    """Invalidate task cache."""
    cache = CacheService()
    key = cache.make_key("task", str(task_id))
    return await cache.delete(key)


# Import asyncio for get_or_set
import asyncio
