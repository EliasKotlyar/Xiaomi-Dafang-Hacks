#!/bin/sh

FILE_NAME="$(date +%Y-%m-%d-%H-%M-%S)"

echo "Content-type: image/jpeg"
echo "Content-Disposition: attachment; filename=\"$FILE_NAME.jpeg\""
echo ""
exec /system/sdcard/bin/getimage
