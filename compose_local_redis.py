#!/usr/bin/env python3
# coding: utf-8
import os
import signal
import sys
import codecs
import subprocess
import click

__author__ = '代码会说话'

gidfile = '/tmp/compose_local_redis.pid'
GROUP_NAME = "compose_local_redis"

@click.group()
def cli():
  pass

@cli.command()
def up():
  if os.path.exists(gidfile):
    click.echo(f'{gidfile} already exists', err=True)
    _try_kill_exists_process_group()
  click.echo(f'before gid {os.getgid()} pid={os.getpid()} ppid={os.getppid()}, pgrp={os.getpgrp()}')
  os.setpgrp()
  click.echo(f'after gid {os.getgid()}')
  gid = os.getppid()
  with codecs.open(gidfile,mode='wt') as f:
    f.write(str(gid))

  cwd = os.path.dirname(__file__)
  for port in range(6380,6383):
    conf = f"conf.d/redis-{port}.conf"
    proc = subprocess.Popen(f'redis-server {conf}',cwd=cwd, shell=True)
  for port in range(26380,26383):
    conf = f"conf.d/sentinel-{port}.conf"
    proc = subprocess.Popen(f'redis-sentinel {conf}',cwd=cwd, shell=True)

def _try_kill_exists_process_group():
  if not os.path.exists(gidfile):
    click.echo(f'{gidfile} not found', err=True)
    return
  with codecs.open(gidfile,mode='rt') as f:
    gid = int(f.read().strip())
  click.echo(f"Terming {gid}")
  try:
    os.kill(gid,signal.SIGTERM)
  except Exception as e:
    click.echo(message=str(e),err=True)
  os.remove(gidfile)

@cli.command()
def down():
  _try_kill_exists_process_group()

if __name__ == '__main__':
  cli()
