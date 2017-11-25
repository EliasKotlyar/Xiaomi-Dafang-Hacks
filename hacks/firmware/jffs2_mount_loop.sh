#!/bin/bash

## Script to mount jffs2 filesystem using mtd kernel modules.
## EMAC, Inc. 2011

if [[ $# -lt 2 ]]
then
    echo "Usage: $0 FSNAME.JFFS2 MOUNTPOINT [ERASEBLOCK_SIZE]"
    exit 1
fi

if [ "$(whoami)" != "root" ]
then
    echo "$0 must be run as root!"
    exit 1
fi

if [[ ! -e $1 ]]
then
    echo "$1 does not exist"
    exit 1
fi

if [[ ! -d $2 ]]
then
    echo "$2 is not a valid mount point"
    exit 1
fi

if [[ "$3" == "" ]]
then
	esize="128"
else
	esize="$3"
fi

# cleanup if necessary
umount /tmp/mtdblock0 &>/dev/null
umount $2 &>/dev/null
modprobe -r jffs2 &>/dev/null
modprobe -r block2mtd &>/dev/null
modprobe -r mtdblock &>/dev/null
sleep 0.25
losetup -d /dev/loop1 &>/dev/null
sleep 0.25

modprobe loop || exit 1
losetup /dev/loop1 "$1" || exit 1
modprobe block2mtd || exit 1
modprobe jffs2 || exit 1
if [[ ! -e /tmp/mtdblock0 ]]
then
    mknod /tmp/mtdblock0 b 31 0 || exit 1
fi

echo "/dev/loop1,${esize}KiB" > /sys/module/block2mtd/parameters/block2mtd

mount -t jffs2 /tmp/mtdblock0 "$2" || exit 1

echo "Successfully mounted $1 on $2"
exit 0
