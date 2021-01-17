## Installation of the microSD bootloader

1. Download the CFW-Binary for your Camera

    Name | SHA3-256 
    --- | --- 
    [Xiaomi DaFang](https://github.com/EliasKotlyar/Xiaomi-Dafang-Hacks/raw/master/hacks/cfw/dafang/cfw-1.3.bin) | d45826d5b471564366b3b9435509df7e8a2c0720656ea2b4bcac6dd0b42cc3eb
    [Xiaomi XiaoFang T20](https://github.com/EliasKotlyar/Xiaomi-Dafang-Hacks/raw/master/hacks/cfw/xiaofang/cfw-1.0.bin) | 333053c3e98af24e0e90746d95e310a3c65b61f697288f974b702a5bcbba48a9
    [Wyzecam V2/Neos SmartCam](https://github.com/EliasKotlyar/Xiaomi-Dafang-Hacks/raw/master/hacks/cfw/wyzecam_v2/cfw-1.1.bin) | ca8fd695fe1903bd12aca2752c86b62c9694430c9c41b2804b006c22e84f409d
    [Wyzecam Pan](https://github.com/EliasKotlyar/Xiaomi-Dafang-Hacks/raw/master/hacks/cfw/wyzecam_pan/cfw-1.0.bin) | f76990d187e763f160f5ad39331d6a3209d3025fe3719cb43c92dbad92cebba2
    Xiaomi XiaoFang T20L | [Start here](/hacks/install_cfw_t10l.md.md)
    Sannce & clones | [Start here](/hacks/install_sannce.md)
    Other Ingenic T10/T20 Device | [Start here](/hacks/newdevices.md)

2. Format your microSD to FAT32. NTFS, EXFAT etc. won't work. Try to use smaller older SD cards like 512 MB or create just a single primary 512 MB partition on it for maximum success rate.
3. Copy the CFW-Binary from step 1 to the formatted microSD card and rename it to "demo.bin". For Wyzecam v3 the filename must be demo_wcv3.bin. There must not be other files on the microSD! This is really important and it won't work if there are any other files on there.
4. Remove the power cable from the camera and plug the microSD card into the camera
5. Hold down the setup button on the camera while
6. Plugging in the USB power cable
7. Keep the setup button pressed for another 10 seconds
8. Wait until the firmware has finished flashing (like 3 minutes). You can disconnect the power as soon as the base starts moving (DaFang/ Wyzecam Pan).
9. Remove the microSD card and power up the camera
10. You should see the blue led shining for 5 seconds (not blinking) **before** the base starts moving (DaFang/ Wyzecam Pan). If not, something went wrong. You should try another microSD card and look at the community tips at the bottom of the page. Start over from step 1.

## Installation of the new Firmware

1. Clone the repository from github. If you are on Windows download the repository as zip file. Make sure nothing gets windows line endings.
2. Copy everything from "firmware_mod" folder into the **root** of the microSD

It should look like this:
```
E:/
├── autoupdate.sh
├── bin
├── config
├── controlscripts
├── driver
├── media
├── run.sh
├── scripts
├── uEnv.bootfromnand.txt
├── uEnv.bootfromsdcard.txt
├── uboot-flash
└── www

```

3. Copy config/wpa_supplicant.conf.dist to config/wpa_supplicant.conf
4. Modify the file config/wpa_supplicant.conf on the microSD card to match your wifi-settings. Make sure wpa_supplicant.conf does not have windows line endings.
5. Insert the microSD card and power up the camera.
6. You can now login at https://dafang or your cameras ip adress with the default credentials root/ismart12

Hint: The security warning about the unsafe https certificate can safely be ignored. A self-signed certificate is automatically generated on your camera during the first startup. By its nature your little camera's own certificate authority is not and never will be among the trusted ones delivered with the major browsers. 

## Updating the microsd-bootloader

Usually, its not required to update the microsd-bootloader. However, if you are using the original firmware, you may be interested in the new version.
You can just update through the MI-Home App.

If you are on original firmware below 5.5.200, you will have to "reflash" the microsd-bootloader afterwards
If you are on original firmware 5.5.200 and update to 5.5.243, the bootloader won't be affected.


## Updating Firmware

If you already have a current custom firmware with custom bootloader installed, you only need to update the content of the microSD card

1. Backup your wpa_config/wpa_supplicant.conf
2. Remove all files from the microSD card
3. Put everything from "firmware_mod" folder into the **root** of the microSD card
4. Copy the backed up wpa_supplicant.conf from step 1 back into the config folder


## Uninstallation

Remove the "run.sh" file from the microSD card.

## Community Tips

1. Use microSD cards smaller than 1 GB such as 512 MB and overwrite the same cards to minimize variations. Formatting only the first 512 MB has also worked for some people.
2. If the bootloader step is not working, double check the microSD card again for files or folders created by the stock firmware. (Sometimes if your timing is off with the setup press the camera will create a time stamp related folder that needs to be deleted before trying again).
3. Make a note of the MAC for the camera and if possible set up DHCP to assign a specific IP address that can be monitored visually in DHCP logs.
4. Start with fewer entries in your wpa_supplicant.conf to isolate WiFi issues.
```
ctrl_interface=/var/run/wpa_supplicant
ctrl_interface_group=0
ap_scan=1

network={
	ssid="enteryourssidherebutrememebertokeepthequotes"
	psk="enteryourpasswordherebutremembertokeepthequotes"
  key_mgmt=WPA-PSK
}
```
5. Inspect you sdcard for logs/startup.log 


### Advanced Installation

Attention: For experienced users/developers only:
[Start here](/hacks/install_sdcard.md)



