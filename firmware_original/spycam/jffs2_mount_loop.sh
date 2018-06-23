#!/bin/sh

if [ -z "$1" ]; then
	echo usage: $0 jffs2_image directory
	exit
fi

if [ -z "$2" ]; then
	echo usage: $0 jffs2_image directory
	exit
fi

modprobe mtdcore
modprobe jffs2

SIZE=`du -h -k $1`
modprobe mtdram total_size=${SIZE} erase_size=256

modprobe mtdchar
modprobe mtdblock

sleep .25

dd if=$1 of=/dev/mtdblock0

mount -t jffs2 /dev/mtdblock0 $2
