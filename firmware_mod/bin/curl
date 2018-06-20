#!/bin/sh
LD_LIBRARY_PATH='/thirdlib:/system/lib:/system/sdcard/lib'
CA_FILE='/system/sdcard/config/ssl/cacert/cacert.pem'
/system/sdcard/bin/curl.bin --cacert ${CA_FILE} "$@"
