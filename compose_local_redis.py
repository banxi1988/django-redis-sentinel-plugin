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
  cwd = os.path.dirname(__file__)
  proc_ids = []
  for port in range(6380,6383):
    conf = f"conf.d/redis-{port}.conf"
    proc = subprocess.Popen(f'redis-server {conf}',cwd=cwd, shell=True)
    proc_ids.append(proc.pid)
  for port in range(26380,26383):
    conf = f"conf.d/sentinel-{port}.conf"
    proc = subprocess.Popen(f'redis-sentinel {conf}',cwd=cwd, shell=True)
    proc_ids.append(proc.pid)

  with codecs.open(gidfile,mode='wt') as f:
    f.writelines([str(pid) for pid in proc_ids])

def _try_kill_exists_process_group():
  if not os.path.exists(gidfile):
    click.echo(f'{gidfile} not found', err=True)
    return
  with codecs.open(gidfile,mode='rt') as f:
    for line in f.readlines():
      if not line:
        continue
      gid = int(line.strip())
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
