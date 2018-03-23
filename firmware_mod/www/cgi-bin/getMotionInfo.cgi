#!/bin/sh
echo "Content-type: text/plain"
echo
color=`/system/sdcard/bin/setconf -g z 2>/dev/null`
if [ "${color}X" == "X" ]
then
    color="0"
fi
echo "osdColor=${color};"

sens=`/system/sdcard/bin/setconf -g m 2>/dev/null`
if [ "${sens}X" == "X" ]
then
    sens="0"
fi
echo "sens=${sens};"

region=`/system/sdcard/bin/setconf -g r 2>/dev/null`
if [ "${region}X" == "X" ]
then
    region="0,0,0,0"
fi
echo "RegionSize=[${region}];"




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
