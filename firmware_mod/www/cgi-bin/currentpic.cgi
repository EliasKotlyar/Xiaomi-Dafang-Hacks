#!/bin/sh
source func.cgi
export LD_LIBRARY_PATH=/system/lib
export LD_LIBRARY_PATH=/thirdlib:$LD_LIBRARY_PATH
WIDTH=$F_width
HEIGHT=$F_height
PARAMS=""


if [ $F_nightvision == 1 ]
  then
    PARAMS="$PARAMS -n"
fi

if [ $F_flip == 1 ]
  then
    PARAMS="$PARAMS -r"
fi



echo "Content-type: image/jpeg"
echo ""
/system/sdcard/bin/v4l2rtspserver-master -fMJPG -W $WIDTH -H $HEIGHT $PARAMS -O /stdout
