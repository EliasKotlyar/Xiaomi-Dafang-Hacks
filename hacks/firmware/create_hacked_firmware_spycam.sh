#!/usr/bin/env bash
FIRMWARE_ROOT=$(pwd)/../../firmware_original/spycam/
TMPDIR=./rootfs
OUTFILE=./rootfs.bin
rm -r $TMPDIR $OUTFILE
unsquashfs -d $TMPDIR $FIRMWARE_ROOT/rootfs.bin
cp ./rcfile.sh $TMPDIR/etc/init.d/rcS
mksquashfs $TMPDIR $OUTFILE -b 1048576 -comp xz -Xdict-size 100%
