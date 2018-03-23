#!/bin/sh
echo "Content-type: text/plain"
echo
echo "osdColor= " `/system/sdcard/bin/setconf -g z`";"
echo "sens=" `/system/sdcard/bin/setconf -g m`";"
echo "RegionSize=[" `/system/sdcard/bin/setconf -g r`"];"
process=`ps -wl| grep v4l2rtspserver-master | grep -v grep`
w=`echo ${process}| awk -F '-W' '{print $2}' | awk '{print $1}'`
if [ "${w}X" == "X" ]
then
    w="1280"
fi
echo "width=${w};"

h=`echo ${process} | awk -F '-H' '{print $2}' | awk '{print $1}'`
if [ "${h}X" == "X" ]
then
    h="720"
fi

echo "height=${h};"
echo
echo
