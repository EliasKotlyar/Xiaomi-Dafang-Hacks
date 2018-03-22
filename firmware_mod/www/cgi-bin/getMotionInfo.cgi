#!/bin/sh
echo "Content-type: text/plain"
echo
echo "osdColor= " `/system/sdcard/bin/setconf -g z`";"
echo "sens=" `/system/sdcard/bin/setconf -g m`";"
echo "RegionSize=[" `/system/sdcard/bin/setconf -g r`"];"
process=`ps -wl| grep v4l2rtspserver-master | grep -v grep`
echo "width="`echo ${process}| awk -F '-W' '{print $2}' | awk '{print $1}'`";"
echo "height="`echo ${process} | awk -F '-H' '{print $2}' | awk '{print $1}'`";"
echo
echo
