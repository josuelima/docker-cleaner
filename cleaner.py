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

class Cleaner:

  def __init__(self, configs):
    self.configs = configs
    self.client  = Client(base_url = self.configs['docker_endpoint'])

    """ Check the connection with docker. End execution if there's no connection """
    try:
      self.client.ping()
    except:
      self.log("Could not connect to Docker. Verify if docker is running or your settings file")
      return

    if self.configs['clear_containers']: self.clear_containers()
    if self.configs['clear_images']: self.clear_images()

  def should_remove_container(self, status):
    """
    Given that we want to remove all obsolet containers (=not running)
    return True to all container statuses not containing 'Up'
    """
    return not status.startswith('Up')

  def remove_container(self, container):
    """ Try to remove container given the container Id """
    try:
      self.client.remove_container(container = container['Id'])
      self.log("Removing container: %s" % container['Id'])
    except:
      self.log_error("container", container)

  def should_remove_image(self, image, containers):
    """
    Determine if the image should be removed if there is no containers based on that
    image running at the momment
    """
    for container in containers:
      if container['Image'] in image['RepoTags']: return False

    return True

  def remove_image(self, image):
    """ Try to remove image given the image Id """
    try:
      self.client.remove_image(image = image['Id'], force = True)
      self.log("Removing image: %s" % image['Id'])
    except:
      self.log_error("image", image)

  def clear_containers(self):
    """ Search for all containers in order to remove those not running """
    for container in self.client.containers(all = True):
      if self.should_remove_container(container['Status']): self.remove_container(container)

  def clear_images(self):
    """
    Search for images in order to remove those which
    doesn't have containers instances running
    """
    running_containers = self.client.containers()

    for image in self.client.images():
      if self.should_remove_image(image, running_containers): self.remove_image(image)

  def log(self, message):
    print message

  def log_error(self, kind, instance):
    self.log("Could not remove %s %s." % (kind, instance['Id']))

if __name__ == '__main__':
  configs = yaml.load(open('settings.yml', 'r'))
  Cleaner(configs)
