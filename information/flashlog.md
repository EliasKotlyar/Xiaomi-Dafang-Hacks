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
