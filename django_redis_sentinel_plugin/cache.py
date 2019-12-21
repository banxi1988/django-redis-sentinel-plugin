from django.utils.module_loading import import_string
from django_redis.cache import RedisCache, DJANGO_REDIS_IGNORE_EXCEPTIONS


class RedisSentinelCache(RedisCache):
    """
    Forces SentinelClient instead of DefaultClient
    """
    def __init__(self, server, params):
        super(RedisCache, self).__init__(params)
        self._server = server
        self._params = params

        options = params.get("OPTIONS", {})
        self._client_cls = options.get("CLIENT_CLASS", "django_redis_sentinel_plugin.client.SentinelClient")
        self._client_cls = import_string(self._client_cls)
        self._client = None

        self._ignore_exceptions = options.get("IGNORE_EXCEPTIONS", DJANGO_REDIS_IGNORE_EXCEPTIONS)
