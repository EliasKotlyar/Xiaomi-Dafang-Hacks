#!/bin/sh

echo "Content-type: image/jpeg"
echo ""
/system/sdcard/bin/getimage |  /system/sdcard/bin/jpegtran -progressive -optimize

