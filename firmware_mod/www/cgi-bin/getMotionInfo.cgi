#!/bin/sh
echo "Content-type: text/plain"
echo
echo -n "enabled= " `/system/sdcard/bin/setconf -g z` |  tr '[:upper:]' '[:lower:]'
echo ";"
echo "sens=" `/system/sdcard/bin/setconf -g m`";"
echo "RegionSize=[" `/system/sdcard/bin/setconf -g r`"];"
