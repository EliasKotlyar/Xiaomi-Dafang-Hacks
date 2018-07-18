## Installation of Open Source Dafang Firmware

1. Install normal Dafanghacks(if not already done) and flash the open source bootloader:
https://github.com/EliasKotlyar/Xiaomi-Dafang-Hacks/blob/master/hacks/flashinguboot.md

2. Partition your Microsd to EXT3

Hint: Use a different MicroSD than your normal Dafang-Hacks one, to debug issues faster.

3. Go into your EXT3 Partition, and clone https://github.com/Dafang-Hacks/rootfs right into it.
Try not to use Windows due to Symlinks etc.

4. Put your credentials on etc/wpa_supplicant.conf in your EXT3 Partition
5. Boot your Dafang 


## Features:
* Complete open source
* Audio should be working now
* No more /system/sdcard/ paths. Everything will have its own place
* RootFS is under git - you can provide every change as a pull request
* IPKG-Manager : Install it using following tutorial from this issue: 
https://github.com/EliasKotlyar/Xiaomi-Dafang-Hacks/issues/542
It will provide a lot of cool software without compiling (git, python etc etc)


## Known issues:
* A lot of Scripts from Dafang-Hacks are broken and need refactoring - mostly paths.






