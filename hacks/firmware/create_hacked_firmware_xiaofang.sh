#!/usr/bin/env bash
FIRMWARE_ROOT=$(pwd)/../../firmware_original/xiaofang/5.6.2.43/
TMPDIR=./rootfs
OUTFILE=./rootfs.bin
rm -r $TMPDIR $OUTFILE
unsquashfs -d $TMPDIR $FIRMWARE_ROOT/rootfs.bin
cp ./rcfile.sh $TMPDIR/etc/init.d/rcS
mksquashfs $TMPDIR $OUTFILE -b 1048576 -comp xz -Xdict-size 100%
./packer.py $FIRMWARE_ROOT/kernel.bin $OUTFILE $FIRMWARE_ROOT/driver.bin $FIRMWARE_ROOT/appfs.bin firmware_hacked.bin
rm -r $TMPDIR $OUTFILE