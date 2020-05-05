#!/bin/sh

echo "Content-type: application/x-binary"
echo 'Content-Disposition: attachment; filename="bootloader.bin"'

echo ""
dd if=/dev/mtd0
