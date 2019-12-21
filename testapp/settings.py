import os
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3"
    },
}

SECRET_KEY = "django_tests_secret_key"
TIME_ZONE = "America/Chicago"
LANGUAGE_CODE = "en-us"
ADMIN_MEDIA_PREFIX = "/static/admin/"
STATICFILES_DIRS = ()

MIDDLEWARE_CLASSES = []


SENTINEL_LOCATIONS = [
    ('sentinel1', '26379'),
    ('sentinel2', '26379'),
    ('sentinel3', '26379'),
]

CACHES = {
    "default": {
        "BACKEND": "django_redis_sentinel_plugin.cache.RedisSentinelCache",
        "LOCATION": SENTINEL_LOCATIONS,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis_sentinel_plugin.client.SentinelClient",
            "SENTINEL_SERVICE_NAME": "rmaster",
            "REDIS_CLIENT_KWARGS": {
                "db": 1
            }
        }
    },
    "doesnotexist": {
        "BACKEND": "django_redis_sentinel_plugin.cache.RedisSentinelCache",
        "LOCATION": SENTINEL_LOCATIONS,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis_sentinel_plugin.client.SentinelClient",
            "SENTINEL_SERVICE_NAME": "rmaster",
            "REDIS_CLIENT_KWARGS": {
                "db": 1
            }
        }
    },
    "sample": {
        "BACKEND": "django_redis_sentinel_plugin.cache.RedisSentinelCache",
        "LOCATION": SENTINEL_LOCATIONS,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis_sentinel_plugin.client.SentinelClient",
            "SENTINEL_SERVICE_NAME": "rmaster",
            "REDIS_CLIENT_KWARGS": {
                "db": 1
            }
        }
    },
    "with_prefix": {
        "BACKEND": "django_redis_sentinel_plugin.cache.RedisSentinelCache",
        "LOCATION": SENTINEL_LOCATIONS,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis_sentinel_plugin.client.SentinelClient",
            "SENTINEL_SERVICE_NAME": "rmaster",
            "REDIS_CLIENT_KWARGS": {
                "db": 1
            }
        },
        "KEY_PREFIX": "test-prefix",
    },
}

INSTALLED_APPS = (
    "django.contrib.sessions",
)
