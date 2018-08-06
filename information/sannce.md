1. Get Digma App from Play Store
2. Connect to Camera using Digma. Go to Settings -> Advanced Settings -> Telnet-Access
3. Connect via Telnet to Camera using following credentials:
root:hslwificam
4. 



``

### Technical Information:
dev:    size   erasesize  name
mtd0: 00040000 00010000 "boot"
mtd1: 00220000 00010000 "kernel"
mtd2: 00340000 00010000 "root"
mtd3: 00240000 00010000 "system"
mtd4: 00010000 00010000 "factory"
mtd5: 00010000 00010000 "param"


Dump Firmware:
dd if=/dev/mtdblock0 of=uboot.bin 
dd if=/dev/mtdblock1 of=kernel.bin
dd if=/dev/mtdblock2 of=rootfs.bin 
dd if=/dev/mtdblock3 of=system.bin 
dd if=/dev/mtdblock4 of=factory.bin 
dd if=/dev/mtdblock5 of=param.bin 


Flash New Bootloader:
fatload mmc 0 0x82000000 sannce.bin
sf probe
sf erase 0x0000 0x40000
sf write 0x82000000 0x00000 0x40000
