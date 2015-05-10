#!/usr/bin/python
#
# DOCKER CLEANER
# Keep your environment clean by removing all obsolete Docker images and containers
#
# For more information visit: github.com/josuelima/docker-cleaner
#
# Author: Josue Lima <josuedsi@gmail.com>

import sys
import yaml
from docker import Client

def should_remove_container(status):
  """
  Given that we want to remove all obsolet containers (=not running)
  return True to all container statuses not containing 'Up'
  """
  return not status.startswith('Up')

def remove_container(container):
  """ Try to remove container given the container Id """
  try:
    client.remove_container(container = container['Id'])
  except:
    log_error("container", container)

def should_remove_image(image, containers):
  """
  Determine if the image should be removed if there is no containers based on that
  image running at the momment
  """
  for container in containers:
    if container['Image'] in image['RepoTags']: return False

  return True

def remove_image(image):
  """ Try to remove image given the image Id """
  try:
    client.remove_image(image = image['Id'], force = True)
  except:
    log_error("image", image)

def clear_containers():
  """ Search for all containers in order to remove those not running """
  for container in client.containers(all = True):
    if should_remove_container(container['Status']): remove_container(container)

def clear_images():
  """
  Search for images in order to remove those which
  doesn't have containers instances running
  """
  running_containers = client.containers()

  for image in client.images():
    if should_delete_image(image, running_containers): remove_image(image)

def log_error(kind, instance):
  print "Could not remove %s %s. Maybe it's running or in a Dead state" % (kind, instance['Id'])

if __name__ == '__main__':
  configs = yaml.load(open('settings.yml', 'r'))

  """ Try to connect to docker endpoint (socket/port) modify in configs.yml """
  try:
    client = Client(base_url = configs['docker_endpoint'])
    client.ping()
  except:
    print "Could not connect to Docker. Verify if docker is running or your configs.yml file"
    sys.exit()

  if configs['clear_containers']: clear_containers()
  if configs['clear_images']: clear_images()