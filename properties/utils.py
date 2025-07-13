from django.core.cache import cache
from django_redis import get_redis_connection
from .models import Property
import logging

logger = logging.getLogger(__name__)


def get_all_properties():
    all_properties = cache.get('all_properties')

    if all_properties is None:
        all_properties = list(Property.objects.all())
        cache.set('all_properties', all_properties, timeout=3600)
    return all_properties


def get_redis_cache_metrics():
    try:
        r = get_redis_connection("default")
        info = r.info()
        hits = info.get("keyspace_hits", 0)
        misses = info.get("keyspace_misses", 0)
        total_requests = hits + misses

        hit_ratio = (hits / total_requests) if total_requests > 0 else 0

        logger.info(f"Cache metrics: hits={hits}, misses={misses}, hit_ratio={hit_ratio}")

        return {
            "hits": hits,
            "misses": misses,
            "hit_ratio": hit_ratio
        }
    except Exception as e:
        logger.error(f"Error fetching Redis metrics: {e}")
        return {}