# coding: utf-8

from django.core.cache.backends.base import get_key_func
from django.core.exceptions import ImproperlyConfigured
from django.utils.module_loading import import_string
from django_redis.client.default import DefaultClient
from django_redis_sentinel_plugin import pool


class SentinelClient(DefaultClient):
    """
    Modifies DefaultClient to work on Sentinel Cluster. URLs passed as servers are no longer master on index 0 and
    slaves the following ones. All URLs should represent the list of sentinels, where order no matters anymore.
    It does not use any cached ConnectionPool as SentinelConnectionPool is for sentinels, not master and slaves.
    The Sentinel client creates a StrictRedis client that performs the connections to actual current elected master or
    slave instances, instead of indexing the URLs for using them as a fixed way to connect to each server.
    This way, through Sentinel client instead of direct creation of StrictRedis from URLs,
    we always have a valid master or slave client (before or after failover).
    New OPTIONS:
        - SENTINEL_SERVICE_NAME (required): Name of monitored cluster
        - SENTINEL_SOCKET_TIMEOUT (optional): Socket timeout for connecting to sentinels, in seconds (accepts float)
    """

    def __init__(self, server, params, backend):
        super(SentinelClient, self).__init__(server, params, backend)

        self._backend = backend
        self._server = server
        self._params = params

        self.reverse_key = get_key_func(params.get("REVERSE_KEY_FUNCTION") or
                                        "django_redis.util.default_reverse_key")

        if not self._server:
            raise ImproperlyConfigured("Missing connections string")

        if not isinstance(self._server, (list, tuple, set)):
            self._server = self._server.split(",")

        self._options = params.get("OPTIONS", {})

        serializer_path = self._options.get("SERIALIZER", "django_redis.serializers.pickle.PickleSerializer")
        serializer_cls = import_string(serializer_path)

        compressor_path = self._options.get("COMPRESSOR", "django_redis.compressors.identity.IdentityCompressor")
        compressor_cls = import_string(compressor_path)

        self._serializer = serializer_cls(options=self._options)
        self._compressor = compressor_cls(options=self._options)

        # Hack: Add sentinels servers as options, to break legacy pool code as less as possible
        self._options.update({"SENTINELS": self._server})
        # Create connection factory for Sentinels
        self.connection_factory = pool.get_connection_factory(options=self._options)


    def get_client(self, write=True, tried=(), show_index=False, force_slave=False,**kwargs):
        """
        Method used for obtain a raw redis client.

        This function is used by almost all cache backend
        operations for obtain a native redis client/connection
        instance.

        If read always looks for a slave (round-robin algorithm, with fallback to master if none available)
        If write then it looks for master
        """
        client =  self.connect(master=write)
        if show_index:
            return client,0
        else:
            return client

    def connect(self, master=True, force_slave=False):
        """
        Given a type of connection master or no master, returns a new raw redis client/connection
        instance. Sentinel always give a valid StrictRedis client with fallback to master in case of no slaves.
        No caching done with clients.
        Even though it can be an improvement, it could lead to stale invalid clients in failovers. Maybe in the future.
        """
        if master:
            return self.connection_factory.connect_master()
        else:
            return self.connection_factory.connect_slave(force_slave)
