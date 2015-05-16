#!/bin/bash
#
# * DOCKER CLEANER
# * Keep your environment clean by removing all obsolete Docker images and containers
# *
# * For more information visit: github.com/josuelima/docker-cleaner
# *
# * This script will install a crontab to run docker-cleaner
# * By default it will run one time a day, every day
# * For more info on crontab: https://help.ubuntu.com/community/CronHowto
# *
# * Author: Josue Lima <josuedsi@gmail.com>

install() {
  path=$(pwd)
  echo "* * * * * /usr/bin/python $path/cleaner.py $path" > crontab.tmp
  crontab -u $USER crontab.tmp
  rm crontab.tmp
}

remove() {
  crontab -r
}

case $1 in
  "remove")
    remove
    ;;
  *)
    install
    ;;
esac
