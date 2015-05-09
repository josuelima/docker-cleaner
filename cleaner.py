#!/usr/bin/python
#
# DOCKER CLEANER
# Keep your docker environment clean by removing all unused docker containers and images
#
# For more information visit: github.com/josuelima/docker-cleaner
#
# Author: Josue Lima <josuedsi@gmail.com>

import sys
from docker import Client

client = Client(base_url='unix://var/run/docker.sock')
containers = client.containers(all = True)

def should_delete_container(status):
  """
  Given that we want to remove all obsolet containers (not running)
  return True to all statuses not containing Up
  """
  return not status.startswith('Up')

def remove_container(container):
  """ Remove container given the container Id"""
  containers.remove_container(container = container['Id'])

for container in containers:
  if should_delete(container['Status']): remove_container(container)