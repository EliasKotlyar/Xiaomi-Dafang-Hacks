# Flashing an open source U-Boot bootloader

## What benefits does this open source bootloader have?

1. You can use H264 FullHD streaming (1920x1080)(on 128 MB devices only)
2. You can boot your own kernel/rootfs from MicroSD
3. You can change your kernel boot-parameters (uEnv.txt)
4. You can flash your NAND using this bootloader
5. It should work on most T20 based devices.
6. The parameters could be changed through fw_printenv
7. It is completely [open source](https://github.com/Dafang-Hacks/uboot)

## What are the disadvantages?
If you flash the wrong u-boot, you can brick your device. I am not taking any responsibility for that!

## Requirements:

1. Determine how much RAM your device has by running the following command via SSH:
```$bash
cat /proc/cmdline 
```

You should get an output like this:

```$bash
console=ttyS1,115200n8 mem=104M@0x0 ispmem=8M@0x6800000 rmem=16M@0x7000000 init=/linuxrc root=/dev/mmcblk0p2 rootwait rootfstype=ext4 rw mtdparts=jz_sfc:256k(boot),2048k(kernel),3392k(root),640k(driver),4736k(appfs),2048k(backupk),640k(backupd),2048k(backupa),256k(config),256k(para),-(flag)
```

Sum up the values from each "mem"-section:

mem + ispmem +rmem = 104M + 8M +16M = 128M

i.e. you have a device with 128 Mb RAM.

## Flashing the U-Boot bootloader:

1. Login via SSH
2. Download the correct [bootloader](https://github.com/Dafang-Hacks/uboot/tree/master/compiled_bootloader) for your device and RAM size.  NOTE: if you are using wget, you need to use the RAW link to the .bin file so that you don't accidentally download a html file.
3. Put the bootloader file in the root of your microsd card `/system/sdcard`. 
4. **Verify the MD5 hash of the file!! Do not skip this step or you may brick your camera!**
5. Write the bootloader to flash
6. Rename the uEnv.bootfromnand.txt in your minisd card root to uEnv.txt

```bash
cd /system/sdcard/

wget https://github.com/Dafang-Hacks/uboot/raw/master/compiled_bootloader/NAME_OF_YOUR_BOOTLOADER_FILE.bin 

md5sum NAME_OF_YOUR_BOOTLOADER_FILE.bin 
```

The `md5sum` command will output a string of hex. That should match the hash listed next to the bin file you downloaded for your [bootloader](https://github.com/Dafang-Hacks/uboot/tree/master/compiled_bootloader) Again, do not proceed unless the MD5 matches the version you downloaded. Now erase and write the bootloader. Do not do anything else between these commands as once you have erased your bootloader. Your device will be unable to boot until you have written a new bootloader.  


```bash
flash_eraseall /dev/mtd0

dd if=/system/sdcard/NAME_OF_YOUR_BOOTLOADER_FILE.bin of=/dev/mtd0

mv uEnv.bootfromnand.txt uEnv.txt

```

For example, if you're flashing dafang_128mb_v2.bin, your command should look like this:

```bash
dd if=/system/sdcard/dafang_128mb_v2.bin of=/dev/mtd0
```

Don't do anything stupid inbetween.
If you crash your camera, you end up without a working bootloader.

## Verify that the U-Boot-Loader works correctly

Reboot your camera

The bootloader is configured to enable the blue led if it has found a valid uEnv.txt during boot up.
Take a look at your LED when it first turns on.

If the led turns yellow -> The default configuration is used.

If the led turns blue -> The custom configuration from uEnv.txt is used.

If the led is not turning blue despite having an uEnv.txt on your microsd - try to format the sdcard as FAT16 and try again.


## Enable FullHD (on 128 Mb devices only):

Open the uEnv.txt file 

```$bash
vi /system/sdcard/uEnv.txt
```
and change the "boot-line" from:

`mem=104M@0x0 ispmem=8M@0x6800000 rmem=16M@0x7000000`

to:

`mem=87M@0x0 ispmem=9M@0x5700000 rmem=32M@0x6000000`

Reboot and check if the bootline has been applied properly using the following command:

```$bash
cat /proc/cmdline
```

## My camera doesn't boot/I have failed to flash the bootloader. What can I do now?
You will need to desolder your bootrom, [reflash it](https://github.com/Dafang-Hacks/spiflasher) and solder it back.
