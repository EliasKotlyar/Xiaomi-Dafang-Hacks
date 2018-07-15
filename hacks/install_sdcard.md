## Installation of Open Source Dafang Firmware

1. Install normal Dafanghacks(if not already done) and flash the open source bootloader:
https://github.com/EliasKotlyar/Xiaomi-Dafang-Hacks/blob/master/hacks/flashinguboot.md

Attention: This step is only working on a Xiaomi Dafang

2. Partition your Microsd with 2 Partitions: 

```
1. Fat16 -> 10MB to 100MB
2. EXT3 -> Your Rootfs
```

You can use normal dafanghacks installation and add a new partition on the end of your microsd.
However note that it needs to be FAT16 or it might not work.
3. Put uEnv.bootfromsdcard.txt from firmware_mod folder to your FAT partition. Rename it to uEnv.txt
4. Check if your uEnv is being used, by inserting the microsd and checking if the blue-led is on. Your camera wont boot yet
5. Get a kernel from the following repository:

https://github.com/Dafang-Hacks/kernel_release/tree/master
Put it onto your FAT-partition and rename it to "kernel.bin"

6. Go into your EXT3 Partition, and clone https://github.com/Dafang-Hacks/rootfs right into it.
Try not to use Windows due to Symlinks etc.

7. Put your credentials on etc/wpa_supplicant.conf in your EXT3 Partition
8. Boot your Dafang :)

## Features:
* Complete open source
* No more /system/sdcard/ paths. Everything will have its own place
* RootFS is under git - you can provide every change as a pull request
* IPKG-Manager : Install it using following tutorial from this issue: 
https://github.com/EliasKotlyar/Xiaomi-Dafang-Hacks/issues/542
It will provide a lot of cool software without compiling (git, python etc etc)


## Known issues:
* Audio is not working - a new kernel driver needs to be compiled
* A lot of Scripts from Dafang-Hacks are broken and need refactoring - mostly paths.






