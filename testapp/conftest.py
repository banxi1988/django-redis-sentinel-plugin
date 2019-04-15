# coding: utf-8
import pytest

__author__ = '代码会说话'


@pytest.fixture()
def cache():
  from django.core.cache import BaseCache
  from django.core.cache import DEFAULT_CACHE_ALIAS,caches
  cache:BaseCache = caches[DEFAULT_CACHE_ALIAS]
  cache.clear()
  return cache