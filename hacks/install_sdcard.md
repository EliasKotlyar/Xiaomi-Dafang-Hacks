## Installation of the Open Source Camera Firmware

1. Install the classic Xiaomi-Dafang-Hacks custom firmware appropriate for your camera (if not already done) and [flash the open source bootloader](https://github.com/EliasKotlyar/Xiaomi-Dafang-Hacks/blob/master/hacks/flashinguboot.md)

2. Partition your MicroSD card to EXT3

Hint: Use a different MicroSD card than your normal Xiaomi-Dafang-Hacks one to debug issues faster.

3. Mount your EXT3 partition and clone https://github.com/Dafang-Hacks/rootfs right into it.
Try not to use Windows due to symlinks, line endings etc.

4. Put your credentials on etc/wpa_supplicant.conf in your EXT3 partition
5. Unmount the MicroSD card
6. Put the MicroSD card in your camera and boot it 


## Features:
* Complete open source
* Audio should be working now
* No more /system/sdcard/ paths. Everything will have its own place.
* RootFS is under git - you can provide every change as a pull request
* IPKG-Manager : Install it using following [tutorial](https://github.com/EliasKotlyar/Xiaomi-Dafang-Hacks/issues/542).
It will provide a lot of cool software without compiling (git, python etc.)

## Known issues:
* A lot of scripts classic Xiaomi-Dafang-Hacks are broken and need refactoring - mostly paths.
