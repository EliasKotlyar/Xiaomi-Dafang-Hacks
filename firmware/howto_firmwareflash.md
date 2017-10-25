## Firmware flashing on Dafang

2. Get a firmware binay and rename it to "demo.bin". There should be no more files in the sdcard
3. Put it into a SD-Card, plug the SDCard into the dafang
3. Hold the Setup-Button on the Dafang
4. Plug in the USB-Cable
5. Wait for 5 minutes


## Format:
```
>file demo_5.5.1.194.bin 
demo_5.5.1.194.bin: u-boot legacy uImage, jz_fw, Linux/MIPS, Firmware Image (Not compressed), 11075584 bytes, Sat Oct 14 03:03:40 2017, Load Address: 0x00000000, Entry Point: 0x00000000, Header CRC: 0xADE7C72E, Data CRC: 0xB57672AD
```

Log of flashing the demo_5.5.1.194.bin File.

```
Hit any key to stop autoboot:  0 
jiabo_do_auto_update!!!!!!!!!!!!!!!!!!!!!!!!
gpio_request lable = sdupgrade gpio = 46
setup_button set long!!!!!!!!!!!!!!!!!!!
Interface:  MMC
  Device 0: Vendor: Man 000002 Snr 751da700 Rev: 1.0 Prod: SA02G
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
  Device 0: Vendor: Man 000002 Snr 751da700 Rev: 1.0 Prod: SA02G
            Type: Removable Hard Disk
            Capacity: 1876.0 MB = 1.8 GB (3842048 x 512)
Filesystem: FAT32 "           "
the manufacturer c8
SF: Detected GD25Q128

reading demo.bin
reading demo.bin
jiabo_au_check_cksum_valid!!!!!!!!!!!!!!!!!!!!!!!!
jiabo_idx=4
misc_init_r before change the blue_gpio
gpio_request lable = blue_gpio gpio = 39
misc_init_r after gpio_request the blue_gpio ret is 39
misc_init_r after change the blue_gpio ret is 0
jiabo_start=40000,jiabo_len=a90000
flash erase...
flash write...
misc_init_r after change the blue_gpio ret is 1
the manufacturer c8
SF: Detected GD25Q128

```
