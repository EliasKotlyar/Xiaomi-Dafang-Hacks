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


if [ -f /var/run/v4l2rtspserver-master-mjpeg.pid ] || [ -f /var/run/v4l2rtspserver-master-h264.pid ]; then
	# Assumption: Whenever a v4l2rtspserver is running, flipping & night mode are already configured
	/system/sdcard/bin/avconv -v 0 -rtsp_transport tcp -y -i rtsp://127.0.0.1:8554/unicast -vframes 1 /tmp/image.jpeg
	cat /tmp/image.jpeg

elif [ -f /var/run/v4l2rtspserver-master-h264-s.pid ]; then
	# Found no way to deal with the segmented stream
	cat /system/sdcard/www/images/sorry.jpg
else
        /system/sdcard/bin/v4l2rtspserver-master -fMJPG -W $WIDTH -H $HEIGHT $PARAMS -O /stdout
fi

