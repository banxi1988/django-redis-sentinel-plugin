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

SENTINEL1_HOST = os.getenv('SENTINEL1_HOST','127.0.0.1')
SENTINEL2_HOST = os.getenv('SENTINEL2_HOST','127.0.0.1')
SENTINEL3_HOST = os.getenv('SENTINEL3_HOST','127.0.0.1')

SENTINEL1_PORT = os.getenv('SENTINEL1_PORT','26380')
SENTINEL2_PORT = os.getenv('SENTINEL2_PORT','26381')
SENTINEL3_PORT = os.getenv('SENTINEL3_PORT','26382')


CACHES = {
    "default": {
        "BACKEND": "django_redis_sentinel.cache.RedisSentinelCache",
        "LOCATION": [
            (SENTINEL1_HOST, SENTINEL1_PORT),
            (SENTINEL2_HOST, SENTINEL2_PORT),
            (SENTINEL3_HOST, SENTINEL3_PORT),
        ],
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis_sentinel.client.SentinelClient",
            "SENTINEL_SERVICE_NAME": "rmaster",
            "REDIS_CLIENT_KWARGS": {
                "db": 1
            }
        }
    },
    "doesnotexist": {
        "BACKEND": "django_redis_sentinel.cache.RedisSentinelCache",
        "LOCATION": [
            (SENTINEL1_HOST, SENTINEL1_PORT),
            (SENTINEL2_HOST, SENTINEL2_PORT),
            (SENTINEL3_HOST, SENTINEL3_PORT),
        ],
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis_sentinel.client.SentinelClient",
            "SENTINEL_SERVICE_NAME": "rmaster",
            "REDIS_CLIENT_KWARGS": {
                "db": 1
            }
        }
    },
    "sample": {
        "BACKEND": "django_redis_sentinel.cache.RedisSentinelCache",
        "LOCATION": [
            (SENTINEL1_HOST, SENTINEL1_PORT),
            (SENTINEL2_HOST, SENTINEL2_PORT),
            (SENTINEL3_HOST, SENTINEL3_PORT),
        ],
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis_sentinel.client.SentinelClient",
            "SENTINEL_SERVICE_NAME": "rmaster",
            "REDIS_CLIENT_KWARGS": {
                "db": 1
            }
        }
    },
    "with_prefix": {
        "BACKEND": "django_redis_sentinel.cache.RedisSentinelCache",
        "LOCATION": [
            (SENTINEL1_HOST, SENTINEL1_PORT),
            (SENTINEL2_HOST, SENTINEL2_PORT),
            (SENTINEL3_HOST, SENTINEL3_PORT),
        ],
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis_sentinel.client.SentinelClient",
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
