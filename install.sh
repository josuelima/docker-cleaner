#!/bin/bash
#
# * DOCKER CLEANER
# * Keep your environment clean by removing all obsolete Docker images and containers
# *
# * For more information visit: github.com/josuelima/docker-cleaner
# *
# * This script will install a crontab to run docker-cleaner
# * It will execute create a cronjob to execute the cleaner every minute
# * For more info on crontab: https://help.ubuntu.com/community/CronHowto
# *
# * This script is just a sugestion. You should customize it accordingly to your needs.
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
