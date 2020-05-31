#!/bin/sh
CONF_FILE_DATE=$(date +%Y-%m-%d_%H-%M-%S)
CONF_FILE_NAME="savedConf-${CONF_FILE_DATE}.tar.gz"
CONF_PATH="/system/sdcard/config"
CONF_DEST="/system/sdcard/DCIM/Config"

if [ ! -d $CONF_DEST ]; then
   mkdir $CONF_DEST
fi

tar -zcf $CONF_DEST/$CONF_FILE_NAME -C $CONF_PATH --exclude='*.dist' .
