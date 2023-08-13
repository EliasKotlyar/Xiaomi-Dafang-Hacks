
# Installation of the Open Source Camera Firmware

1. Install the classic Xiaomi-Dafang-Hacks custom firmware appropriate for your camera (if not already done) and [flash the open source bootloader](https://github.com/EliasKotlyar/Xiaomi-Dafang-Hacks/blob/master/hacks/flashinguboot.md)

2. Partition your MicroSD card to EXT3: 

To achieve this you can use linux tools like fdisk, parted or (in a graphical environment) gparted, combined with the use of mkfs.ext3 .

The following example is an 8GB SD card wih a first primary partition of 512MB for allocating the operating sistem, and a second one with the rest of the space, both formatted as EXT3:
```
# fdisk -l /dev/sdb
Disk /dev/sdb: 7.41 GiB, 7958691840 bytes, 15544320 sectors
Disk model: Storage Device  
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disklabel type: dos
Disk identifier: 0x41289c77

Device     Boot   Start      End  Sectors  Size Id Type
/dev/sdb1  *       2048  1050623  1048576  512M 83 Linux
/dev/sdb2       1050624 15544319 14493696  6.9G 83 Linux

```
*Hint: Use a different MicroSD card than your normal Xiaomi-Dafang-Hacks one to debug issues faster.*

3. Mount your EXT3 first partition and clone the content of <https://github.com/Dafang-Hacks/rootfs> right into it
**Try not to use Windows due to symlinks, line endings etc.**

4. Put your credentials on etc/wpa_supplicant.conf in your EXT3 partition, refer to the [installation manual](https://github.com/EliasKotlyar/Xiaomi-Dafang-Hacks/blob/master/hacks/install_cfw.md)

5. Depending on the camera version you have to copy the appropiate uEnv_\<model\>.txt file onto an uEnv.tx file at the root-level of de MicroSD Card. For example, for a Dafang Cam with 128MB of memory, you have to do the following:
```
    # mv uEnv_dafang128.txt uEnv.txt
```

6. Depending on the camera version you have to load the appropriate wireless card driver, this is done commenting out the startup script located in  etc/init.d/rcS, in the EXT3 partition of the microSD card. Locate the following section of the  mentioned file:

```
# insmod /lib/modules/$KERNEL_VERSION/rtl8189es.ko rtw_initmac="$MAC" # Uncomment for Dafang
# insmod /lib/modules/$KERNEL_VERSION/rtl8189fs.ko rtw_initmac="$MAC" # Uncomment for XiaoFang s1 && Wyzecam V2
# insmod /lib/modules/$KERNEL_VERSION/mt7601Usta.ko # Uncomment for Sannce

```
And remove the first **\#** of the line that matches your camera version (Look at the comments at the end of the line)

For example, for a Dafang 128MB of memory CAM it will look like this:
```
insmod /lib/modules/$KERNEL_VERSION/rtl8189es.ko rtw_initmac="$MAC" # Uncomment for Dafang
# insmod /lib/modules/$KERNEL_VERSION/rtl8189fs.ko rtw_initmac="$MAC" # Uncomment for XiaoFang s1 && Wyzecam V2
# insmod /lib/modules/$KERNEL_VERSION/mt7601Usta.ko # Uncomment for Sannce
```

7. Unmount the MicroSD card

8. Put the MicroSD card in your camera and boot it
9. Optional: If you create a second partition, you can mount it in the cam operating system,.For that, connect though ssh to the cam and create a mount point, for example located in /media/storage, and add the proper line to the /etc/fstab file. The following is an example of the procedure:
 
```
# mkdir /media/storage

# vi /etc/fstab
{ ... content os /etc/fstab ommited ... }
#Line added to the etc/fstab file
/dev/mmcblk0p2  /media/storage  ext3 	rw,relatime	0	0
{ ..end of /etc/fstab }

# mount /media/storage
``` 
*Note: The vi command is for editing the /etc/fstab file you dont have to add the comments enclosed by brackets { ... .... }* only th line that begins with /dev is necessary to be **added** an the end of the file
*Note 2: The mount command is only needed this time, the next reboot it wil be mounted automatically*


## Features



* Complete open source
* Audio should be working now
* No more /system/sdcard/ paths. Everything will have its own place.
* RootFS is under git - you can provide every change as a pull request
* IPKG-Manager : Install it using following [tutorial](https://github.com/EliasKotlyar/Xiaomi-Dafang-Hacks/issues/542).
It will provide a lot of cool software without compiling (git, python etc.)

## Known issues

* A lot of scripts classic Xiaomi-Dafang-Hacks are broken and need refactoring - mostly paths.

## Troubleshooting
If you have problems booting up and cannot connect to IP of the cam, remove th card form the camera al mount it on a PC, locate the var/log/startup.log on the root of the MicroSD Card and read it. Also you can put content inside the etc/init.d/rcS, like :
```
echo "CUSTOM LOG: Loading wireless drivers from /lib/modules/$KERNEL_VERSION" >> $LOGPATH

```

To see your custom boot log messages.
