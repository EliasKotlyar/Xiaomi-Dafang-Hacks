#!/bin/sh
source func.cgi
export LD_LIBRARY_PATH=/system/sdcard/lib
CMD=$F_cmd

/system/sdcard/bin/USBMissileLauncherUtils "$CMD" -S 200

echo "Content-type: text/html"
echo ""
