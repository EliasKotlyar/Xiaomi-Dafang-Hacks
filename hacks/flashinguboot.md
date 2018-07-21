# Flashing an Open-Source U-Boot

## What benefits does this open source bootloader have?

1. You can use H264 FullHD Streaming (1920x1080)(128MB devices only)
2. You can boot your own kernel/rootfs/whatever from MicroSD
3. You can change your kernel boot-parameters (uEnv.txt)
4. You can flash your NAND using this bootloader
5. It should work on nearly all T20 based devices.
6. The parameters could be changed through fw_printenv
7. It is completely open source - Check the source here: https://github.com/Dafang-Hacks/uboot


## What are the disadvantages?
You can brick your device, if you flash the wrong u-boot. I am not taking any responsibility for that!

## Requirements:

1. Find out how much RAM your device have by running following command via SSH:
```$bash
[root@DafangHacks:~]# cat /proc/cmdline 
```


You will get an output similar to that:

```$bash
console=ttyS1,115200n8 mem=104M@0x0 ispmem=8M@0x6800000 rmem=16M@0x7000000 init=/linuxrc root=/dev/mmcblk0p2 rootwait rootfstype=ext4 rw mtdparts=jz_sfc:256k(boot),2048k(kernel),3392k(root),640k(driver),4736k(appfs),2048k(backupk),640k(backupd),2048k(backupa),256k(config),256k(para),-(flag)
```

Count together the values from each "mem"-section:

mem = 104M

rmem = 16M

ispmem = 8M

-> Together 128M -> You have a 128Mb Ram Device

## Flashing U-Boot:

1. Login via SSH
2. Get one of the following Files according to your amount of Ram & your device:
https://github.com/Dafang-Hacks/uboot/tree/master/compiled_bootloader

3. Put the File to your microsd
4. **Verify the MD5 Hash of the file!! Do not skip this step, or you may brick your cam!**
3. Run following command

```bash
flash_eraseall /dev/mtd0
dd if=<filename.bin> of=/dev/mtd0
```


## Verifying the U-Boot-Loader
1. Get a uEnv.bootfromnand.txt file from*__* this repository. 
1. Rename the uEnv.bootfromnand.txt to uEnv.txt
2. Boot your camera

The bootloader is configured to enable the blue-led if it takes the configuration from the uEnv.txt as soon as it boots up.
Take a look at your LED when it first turns on.

If it turns yellow -> The normal configuration is being taken

If it turns blue -> Custom Configuration from uEnv.txt is being taken.

If its not turning blue despite that you have a uEnv.txt on your microsd - try to format it as FAT16 and try again


## Turning on FULLHD(128Mb Devices only):

Open up the uEnv.txt file and change the "boot-line" from

mem=104M@0x0 ispmem=8M@0x6800000 rmem=16M@0x7000000

to

mem=87M@0x0 ispmem=9M@0x5700000 rmem=32M@0x6000000
 
 
Check if its being applied using the following command:

[root@DafangHacks:~]# cat /proc/cmdline



## My camera doesn't boot/I have failed flashing the bootloader - what now?
You will need to desolder your chip, reflash it and solder it back.
Here is information about how to do it:
https://github.com/Dafang-Hacks/spiflasher
