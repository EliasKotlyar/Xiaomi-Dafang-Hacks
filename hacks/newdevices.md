### Installation on generic T10/T20 Devices

It should be possible to install this hack to any T10 or T20 based devices. If you want to do so, begin with the porting tutorial:

The process consists of 3 steps:

### Information gathering
1. Disassemble the Device and make a lot of photos. 
2. Connect via TTL to the camera. You can use the following blog article as a reference: https://nm-projects.de/2016/12/hacking-digoo-bb-m2-mini-wifi-part-1-identify-the-serial-interface/
3. Get root access: https://github.com/EliasKotlyar/Xiaomi-Dafang-Hacks/blob/master/hacks/getroot.md
4. Dump the firmware:
https://github.com/EliasKotlyar/Xiaomi-Dafang-Hacks/blob/master/hacks/firmware-dump.md
5. Dump a bootlog of your camera
6. Collect all the information together in a github issue in this repository

### Finding a method to boot into a CFW:
1. Check the bootlog of your camera. Its often has an option to flash the whole firmware. Often it can be triggered by having a special file on your microsd / holding some button.

In Xiaomi based devices its often called "demo.bin"
```
Hit any key to stop autoboot:  0 
jiabo_do_auto_update!!!!!!!!!!!!!!!!!!!!!!!!
gpio_request lable = sdupgrade gpio = 46
setup_button set long!!!!!!!!!!!!!!!!!!!
Interface:  MMC
  Device 0: Vendor: Man 000002 Snr 751da700 Rev: 1.0 Prod: SA02G�
            Type: Removable Hard Disk
            Capacity: 1876.0 MB = 1.8 GB (3842048 x 512)
Filesystem: FAT32 "           "
the manufacturer c8
SF: Detected GD25Q128

reading demo.bin
the manufacturer c8
SF: Detected GD25Q128



jiabo_do_auto_update!!!!!!!!!!!!!!!!!!!!!!!!
gpio_request lable = sdupgrade gpio = 46
setup_button set long!!!!!!!!!!!!!!!!!!!
Interface:  MMC
  Device 0: Vendor: Man 000002 Snr 751da700 Rev: 1.0 Prod: SA02G�
            Type: Removable Hard Disk
            Capacity: 1876.0 MB = 1.8 GB (3842048 x 512)
Filesystem: FAT32 "           "
the manufacturer c8
SF: Detected GD25Q128
```

Other manufacturers have often some other routine like:
```
Hit any key to stop autoboot:  0 
>>>>Auto upgrade start!
Interface:  MMC
  Device 0: Vendor: Man 000003 Snr 700a2401 Rev: 15.9 Prod: SC16G�
            Type: Removable Hard Disk
            Capacity: 15193.5 MB = 14.8 GB (31116288 x 512)
Filesystem: FAT16 "           "
the manufacturer c2
SF: Detected MX25L128**E

reading uImage.uvc
** Unable to read file uImage.uvc **
read uImage.uvc sz -1 hdr 64
reading FIRMWARE_DS202.bin
** Unable to read file FIRMWARE_DS202.bin **
read FIRMWARE_DS202.bin sz -1 hdr 64
reading FIRMWARE_DS202_F.Bin
** Unable to read file FIRMWARE_DS202_F.Bin **
read FIRMWARE_DS202_F.Bin sz -1 hdr 64
>>>>Auto upgrade Fail!
the manufacturer c2
SF: Detected MX25L128**E

--->probe spend 4 ms
SF: 2097152 bytes @ 0x40000 Read: OK
--->read spend 272 ms
```

If there is a possibility of upgrading the firmware trough the bootloader, you can  try to modify the rootfs and include some script to boot from the microsd. Here is a tutorial. You will probably need to adjust the scripts:
![Tutorial](/hackshowto_modfirmware.md)



2. If there is no option for an upgrade of your firmware, you can still try to flash something on your device by stopping the bootloader and flashing a different bootloader, which can boot from microsd.

To do so, please collect the following informations:
1. Which SOC is your device running? T10 or T20?
2. How much ram does the device has? 

Both informations can be collected from the bootlog.

As soon as you know how much ram it has, you can try to flash a different bootloader by stopping the bootloader and using the following commands:
First you need to collect a bootloader which is suitable for your device. You can find different bootloaders here:
https://github.com/Dafang-Hacks/uboot/tree/master/compiled_bootloader

Ask for help if needed.

Here are the commands for flashing the bootloader:
```
fatls mmc 0:1
fatload mmc 0:1 0x80600000 bootloader.bin
sf probe
sf update 0x80600000 0x0 0x40000
```

##Attention: You may brick your camera!! Please consider that before flashing a different bootloader. We are not responsible for a brick. ##

3. Booting into CFW: As soon as you have a possibility to boot your device, you can try to boot into the CFW. Use one of the tutorials depending on your booting method.


