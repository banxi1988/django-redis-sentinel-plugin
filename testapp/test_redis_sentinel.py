# coding: utf-8
import os
import time

from django_redis.cache import RedisCache
from redis import StrictRedis

from django_redis_sentinel.cache import RedisSentinelCache
from django_redis_sentinel.client import SentinelClient
from django_redis_sentinel.pool import SentinelConnectionFactory

__author__ = '代码会说话'

import pytest
from redis.sentinel import Sentinel
SENTINEL1_HOST = os.getenv('SENTINEL1_HOST','127.0.0.1')
SENTINEL2_HOST = os.getenv('SENTINEL2_HOST','127.0.0.1')
SENTINEL3_HOST = os.getenv('SENTINEL3_HOST','127.0.0.1')

SENTINEL1_PORT = os.getenv('SENTINEL1_PORT','26380')
SENTINEL2_PORT = os.getenv('SENTINEL2_PORT','26381')
SENTINEL3_PORT = os.getenv('SENTINEL3_PORT','26382')

sentinel = Sentinel([
  (SENTINEL1_HOST, SENTINEL1_PORT),
  (SENTINEL2_HOST, SENTINEL2_PORT),
  (SENTINEL3_HOST, SENTINEL3_PORT),
], socket_timeout=0.1)

MASTER_NAME = 'rmaster'
def test_redis_basic_sentinel_function():
  master_info = sentinel.discover_master(MASTER_NAME)
  print("master_info:", master_info)
  slave_infos = sentinel.discover_slaves(MASTER_NAME)
  print("slave_infos:", slave_infos)

  master = sentinel.master_for(MASTER_NAME, socket_timeout=0.1)
  slave = sentinel.slave_for(MASTER_NAME, socket_timeout=0.1)

  author = "banxi"
  master.set('author', author)
  r_author = slave.get('author')
  print('author:', str(r_author))
  assert r_author.decode('utf-8') == author

def encode_key(key:str,prefix:str,version:str):
  return f'{prefix}:{version}:{key}'

def decode_key(key:str):
  return key.split(':',2)[-1]

def test_django_redis_custom_key_fun(cache:RedisCache):
  assert isinstance(cache,RedisSentinelCache)
  for key in ["foo-aa", "foo-ab", "foo-bb", "foo-bc"]:
    cache.set(key, "foo")
  res = cache.delete_pattern("*foo-a*")
  assert res

  keys = cache.keys("foo*")
  assert  set(keys) ==  {"foo-bb", "foo-bc"}
  # ensure our custom function was actually called
  try:
    assert (set(k.decode('utf-8') for k in cache.raw_client.keys('*')),
            {':1:foo-bc', ':1:foo-bb'})
  except (NotImplementedError, AttributeError):
    # not all clients support .keys()
    pass

def test_setnx(cache:RedisCache):
  assert isinstance(cache,RedisSentinelCache)
  key = 'test_key_nx'
  cache.delete(key)
  assert cache.get(key) is None
  assert cache.set(key,1, nx=True)
  assert not cache.set(key,2, nx=True)
  assert cache.get(key) == 1
  cache.delete(key)
  assert cache.get(key) is None

def test_setnx_timeout(cache:RedisCache):
  assert isinstance(cache,RedisSentinelCache)
  # test timeout works
  key = 'test_key_nx2'
  assert cache.set(key, 1, timeout=2,nx=True)
  time.sleep(3)
  assert cache.get(key) is None
  # test timeout will not affect key,if it was there
  cache.set(key, 1)
  assert not cache.set(key,2, timeout=2, nx=True)
  time.sleep(3)
  assert cache.get(key) == 1
  cache.delete(key)
  assert cache.get(key) is None

def test_save_and_int(cache:RedisCache):
  assert isinstance(cache,RedisSentinelCache)
  key = 'test_key_3'
  cache.set(key, 2)
  res = cache.get(key, 'astr')
  assert res == 2

def test_save_str(cache:RedisCache):
  assert isinstance(cache,RedisSentinelCache)
  key = 'test_key_4'
  str1 = "hello" * 1000
  cache.set(key, str1)
  assert cache.get(key) == str1
  str2 = "2"
  cache.set(key, str2)
  assert cache.get(key) == str2

  str3 = "some chinese 有一些中文"
  cache.set(key, str3)
  assert cache.get(key) == str3

def test_save_dict(cache:RedisCache):
  key = 'test_key_5'
  d1 = {"id":1,"name":"CodeTalks","memo":"生活真美好"}
  cache.set(key, d1)
  assert cache.get(key) == d1


def test_persist(cache:RedisCache):
  key = 'test_key_6'
  cache.set(key, 'bar', timeout=20)
  cache.persist(key)
  assert cache.ttl(key) is None

def test_expire(cache:RedisCache):
  key = 'test_key_7'
  cache.set(key, 'bar', timeout=None)
  cache.expire(key, 20)
  ttl = cache.ttl(key)
  assert 18 < ttl <= 20


def test_lock(cache:RedisCache):
  key = 'test_key_8'
  lock = cache.lock(key)
  lock.acquire(blocking=True)
  assert cache.has_key(key)
  lock.release()
  assert not cache.has_key(key)

def test_master_slave_switching(cache:RedisSentinelCache):
  import time
  client:SentinelClient = cache.client
  master1:StrictRedis = client.get_client(write=True)
  master1_replication1 = master1.info('replication')
  assert master1_replication1['role'] == 'master'
  pool:SentinelConnectionFactory = client.connection_factory
  sentinel_manager:Sentinel = pool._sentinel
  sentinel1 =  sentinel_manager.sentinels[0]
  sentinel1.execute_command(f'sentinel failover {pool.service_name} ')
  time.sleep(3) # 等待 sentinel 切换完成

  master1_replication2 = master1.info('replication')
  assert master1_replication2['role'] == 'master'

  master2 : StrictRedis = client.get_client(write=True)
  master2_replication1 = master2.info('replication')
  master1_slaves = [slave for key,slave in master1_replication1.items() if key.startswith("slave")]
  master2_slaves = [slave for key,slave in master2_replication1.items() if key.startswith("slave")]
  assert master1_slaves != master2_slaves

  # 关闭当前主 master 等待被动切换
  master2_server = master2.info('server')
  master2_process_id = master2_server['process_id']
  assert master2_process_id
  import os,signal
  os.kill(master2_process_id,signal.SIGTERM)
  time.sleep(15)
  master3 : StrictRedis = client.get_client(write=True)
  master3_replication1 = master3.info('replication')
  master3_slaves = [slave for key,slave in master3_replication1.items() if key.startswith("slave")]

  assert master2_slaves != master3_slaves

