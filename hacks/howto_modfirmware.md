## Unpack Firmware

Use unpacker.py with the firmware:

```
./unpacker.py demo_5.5.1.194.bin
```


## Pack Firmware

Install requirements
```
sudo apt-get install u-boot-tools
```

Use packer.py with the firmware files:

```
./packer.py kernel.bin rootfs.bin driver.bin appfs.bin new_firmware.bin
```


## File Formats used

Name | Format 
--- | --- 
uboot.bin | Uboot-Binary
kernel.bin| Kernel Image
rootfs.bin| SquashFS
driver.bin| SquashFS
appfs.bin| JFFS2
backupk.bin| Backup Kernel
backupd.bin| Backup Driver
backupa.bin| Backup Appfs
config.bin| JFFS2
para.bin| JFFS2
flag.bin| Textfile


## Extract Kernel:
The Kernel is compressed using lzma. Use the following Instructions for extracting it:
https://stackoverflow.com/questions/37672417/getting-kernel-version-from-the-compressed-kernel-image


## Extract JFFS2:
Use following Tutorial:
http://wiki.emacinc.com/wiki/Mounting_JFFS2_Images_on_a_Linux_PC

## Extract SquashFS

https://unix.stackexchange.com/questions/80305/mounting-a-squashfs-filesystem-in-read-write