#!/usr/bin/python
#
# DOCKER CLEANER
# Keep your environment clean by removing all obsolete Docker images and containers
#
# For more information visit: github.com/josuelima/docker-cleaner
#
# Author: Josue Lima <josuedsi@gmail.com>

import sys
from docker import Client

client = Client(base_url='unix://var/run/docker.sock')

def should_remove_container(status):
  """
  Given that we want to remove all obsolet containers (=not running)
  return True to all container statuses not containing Up
  """
  return not status.startswith('Up')

def remove_container(container):
  """ Remove container given the container Id"""
  #containers.remove_container(container = container['Id'])
  print "remove this"

def should_remove_image(image, containers):
  """
  Determine if the image should be removed if there is no containers based on that
  image running at the momment
  """
  for container in containers:
    if container['Image'] in image['RepoTags']: return False

  return True

def clear_containers():
  """ Search for all containers to remove those not running"""
  for container in client.containers(all = True):
    if should_remove_container(container['Status']): remove_container(container)

def clear_images():
  """
  Search for images to remove those which
  doesn't have containers instances running
  """
  running_containers = client.containers()

  for image in client.images():
    if should_delete_image(image, running_containers): remove_image(image)