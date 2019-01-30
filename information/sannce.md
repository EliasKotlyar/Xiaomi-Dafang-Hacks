# Installation of the open source bootloader on generic devices:

1. Get Digma App from Play Store 

Link: https://play.google.com/store/apps/details?id=digma.p2pipcam&hl=de
2. Connect to Camera using Digma. Go to Settings -> Advanced Settings -> Telnet-Access and enable Telnet

3. Connect via Telnet to Camera using following credentials:

root:hslwificam

4. Find out how much ram your device have and which processor its using. Check if there is already an bootloader available here:
https://github.com/Dafang-Hacks/uboot/tree/master/compiled_bootloader

If there is an bootloader available, ask for help in an issue. Provide some dumps if possible.

5. Put the bootloader-file to your microsd and rename it to "bootloader.bin"

6. Verify the MD5 Hash of the bootloader file!! Do not skip this step, or you may brick your cam!

7. Run following command in shell

```
cd /mnt/
flash_eraseall /dev/mtd0
dd if=bootloader.bin of=/dev/mtd0
```

8. Format your SDcard to Ext3

9. Put the content of the following Repository into Root Directory of the SdCard
https://github.com/Dafang-Hacks/rootfs

10. Modify the wpa_supplicant.conf file in /etc folder to match your Wifi-Settings. Also uncomment the instructions for Sannce in etc/init.d/rcS







### Experimental:
9. Install entware:
wget -O - http://pkg.entware.net/binaries/mipsel/installer/installer.sh | sh




If your camera get stuck at the first command(like SANNCE Devices)

### New Hardware

Use following Command to dump the layout:
```$xslt
cat /proc/mtd 
dev:    size   erasesize  name
mtd0: 00040000 00010000 "boot"
mtd1: 00220000 00010000 "kernel"
mtd2: 00340000 00010000 "root"
mtd3: 00240000 00010000 "system"
mtd4: 00010000 00010000 "factory"
mtd5: 00010000 00010000 "param"

Dump Firmware according to the layout
dd if=/dev/mtdblock0 of=uboot.bin 
dd if=/dev/mtdblock1 of=kernel.bin
dd if=/dev/mtdblock2 of=rootfs.bin 
dd if=/dev/mtdblock3 of=system.bin 
dd if=/dev/mtdblock4 of=factory.bin 
dd if=/dev/mtdblock5 of=param.bin 
```

Then zip everything and provide the zip in the issue





