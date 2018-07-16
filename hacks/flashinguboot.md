# Flashing an Open-Source U-Boot

## Everything that you are doing is at your own risk. Please do not try to use this, unless you can accept a hardbrick! Its highly recommended to avoid this on new hardware.


## What benefits does this open source bootloader have?

1. You can use H264 FullHD Streaming (1920x1080)
2. You can boot your own kernel/rootfs/whatever from MicroSD
3. You can change your kernel boot-parameters (uEnv.txt)
4. You can flash your NAND using this bootloader
5. It should work on nearly all T20 based devices.
6. The parameters could be changed through fw_printenv
7. It is completely open source - Check the source here: https://github.com/Dafang-Hacks/uboot

## What are the disadvantages?
1. Its not stock - maybe some optimisations to specific devices are missing
2. There is no ethernet support on the bootloader level. You cannot use TFTP to 
flash back your NAND. However, you can still use a serial interface and/or the microsd slot.

## HowTo flash the bootloader on a Xiaomi Dafang:

1. Login via SSH
2. Run

```bash
cd /system/sdcard/uboot-flash
./flash_opensource_t20.sh
```

## HowTo flash the bootloader on other Devices:

....Coming soon...

## HowTo return to the stock bootloader (Dafang only):
1. Login into SSH
2. Run

```bash
cd /system/sdcard/uboot-flash
./flash_original_dafang.sh
```

## My camera doesn't boot/I have failed flashing the bootloader - what now?
You will need to desolder your chip, reflash it and solder it back.
Here is information about how to do it:
https://github.com/Dafang-Hacks/spiflasher
