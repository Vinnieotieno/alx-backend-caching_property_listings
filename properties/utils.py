from django.core.cache import cache
from django_redis import get_redis_connection
from .models import Property
import logging

logger = logging.getLogger(__name__)


def get_all_properties():
    """
    Retrieve all properties, cached in Redis for 1 hour.
    """
    properties = cache.get('all_properties')

    if properties is None:
        logger.info("Cache miss → querying database.")
        properties = list(Property.objects.values())
        cache.set('all_properties', properties, timeout=3600)
    else:
        logger.info("Cache hit → returning cached data.")

    return properties


def get_redis_cache_metrics():
    """
    Collect Redis cache hit/miss metrics and compute hit ratio.
    """
    conn = get_redis_connection("default")
    info = conn.info()

    hits = info.get("keyspace_hits", 0)
    misses = info.get("keyspace_misses", 0)
    total = hits + misses

    hit_ratio = (hits / total) * 100 if total > 0 else 0

    logger.info(f"Redis Cache Hits: {hits}")
    logger.info(f"Redis Cache Misses: {misses}")
    logger.info(f"Redis Cache Hit Ratio: {hit_ratio:.2f}%")

    return {
        "hits": hits,
        "misses": misses,
        "hit_ratio": hit_ratio,
    }
