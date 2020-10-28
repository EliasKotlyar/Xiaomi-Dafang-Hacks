#!/bin/sh

## Get OSD-Information
if [ -f /system/sdcard/config/osd.conf ]; then
	. /system/sdcard/config/osd.conf > /dev/null 2>/dev/null
	AXIS=""
	# Call setconf only if we have something to set, to avoid outputing error messages
	[ "${DISPLAY_AXIS}" = true ] && AXIS=$(/system/sdcard/bin/motor -d s | sed '3d' | awk '{printf ("%s ",$0)}' | awk '{print " X="$2,"Y="$4}')
	[ "${ENABLE_OSD}" = true ] && /system/sdcard/bin/setconf -k o -v "${OSD}${AXIS}" 2>/dev/null
	[ ! -z "${COLOR}" ] && /system/sdcard/bin/setconf -k c -v ${COLOR} 2>/dev/null
	[ ! -z "${SIZE}" ] && /system/sdcard/bin/setconf -k s -v ${SIZE} 2>/dev/null
	[ ! -z "${POSY}" ] && /system/sdcard/bin/setconf -k x -v ${POSY} 2>/dev/null
	[ ! -z "${FIXEDW}" ] && /system/sdcard/bin/setconf -k w -v ${FIXEDW} 2>/dev/null
	[ ! -z "${SPACE}" ] && /system/sdcard/bin/setconf -k p -v ${SPACE} 2>/dev/null
	[ ! -z "${FONTNAME}" ] && /system/sdcard/bin/setconf -k e -v ${FONTNAME} 2>/dev/null
else
	/system/sdcard/bin/setconf -k o -v ""
fi
