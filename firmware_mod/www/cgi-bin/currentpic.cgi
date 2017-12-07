#!/bin/sh
source func.cgi
WIDTH=$F_width
HEIGHT=$F_height
NIGHTVISION=$F_nightvision
export LD_LIBRARY_PATH=/system/lib
export LD_LIBRARY_PATH=/thirdlib:$LD_LIBRARY_PATH

echo "Content-type: image/jpeg"
echo ""
/system/sdcard/bin/jpegSnap -w $WIDTH -h $HEIGHT -n $NIGHTVISION
