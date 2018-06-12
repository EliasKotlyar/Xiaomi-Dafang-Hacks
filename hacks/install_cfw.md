## Installation of the microSD bootloader

1. Download the CFW-Binary for your Camera

    Name | SHA3-256 
    --- | --- 
    [Xioami Dafang](/hacks/cfw/dafang/cfw-1.3.bin) | d45826d5b471564366b3b9435509df7e8a2c0720656ea2b4bcac6dd0b42cc3eb
    [Xioami Xiaofang T20](/hacks/cfw/xiaofang/cfw-1.0.bin) | 333053c3e98af24e0e90746d95e310a3c65b61f697288f974b702a5bcbba48a9
    [Wyzecam V2](/hacks/cfw/wyzecam_v2/cfw-1.1.bin) | ca8fd695fe1903bd12aca2752c86b62c9694430c9c41b2804b006c22e84f409d
    [Wyzecam Pan](/hacks/cfw/wyzecam_pan/cfw-1.0.bin) | f76990d187e763f160f5ad39331d6a3209d3025fe3719cb43c92dbad92cebba2


2. Format your microSD to FAT32. NTFS, EXFAT etc. won't work.
3. Copy the CFW-Binary from step 1 to the formated microSD and rename it to "demo.bin". There should be no other files on the microSD! This is really important and it won't work if there are any other files on there.
4. Shutdown the Dafang camera, remove the power cable and plug the microSD into the Dafang
5. Hold down the setup button on the Dafang camera while
6. Plugging in the USB power cable
7. Keep setup button for another 10 seconds
8. Wait until the firmware has finished flashing (like 3 minutes). Disconnect the power as soon as the base starts moving.
9. Remove the microSD and try to start the Dafang camera
10. You should see the blue led shining up for 5 seconds (not blinking) **before** the base starts moving. If not, something went wrong. You should try another microSD. Start over from step 1.

## Installation of the new Firmware

1. Clone the repository from github. If you are on windows download the repository as zip file.
2. Copy everything from "firmware_mod" folder into the **root** of the microSD

It should look like this:
```
E:/
├── bin
├── config
├── run.sh
├── scripts
└── www

```

3. Copy config/wpa_supplicant.conf.dist to config/wpa_supplicant.conf
4. Modify the file config/wpa_supplicant.conf on the microSD to match your wifi-settings
5. Insert the microSD and start the camera.

## Updating the microsd-bootloader

Usually, its not required to update the microsd-bootloader. However, if you are using the original Firmware, you may be interessted in the new Version.
You can just update trough the MI-Home App.

If you are on original Firmware below 5.5.200, you will have to "reflash" the microsd-bootloader afterwards
If you are on original Firmware 5.5.200 and update to 5.5.243, the bootloader wont be affected.


## Updating Firmware

If you already have a current custom firmware with custom bootloader installed, you only need to update the content of the microSD

1. Backup your wpa_config/wpa_supplicant.conf
2. Remove all files from the microSD
3. Put everything from "firmware_mod" folder into the **root** of the microSD
4. Copy the backed up wpa_supplicant.conf from step 1 back into the config folder

## Uninstallation

Remove the "run.sh" file from microSD.

## Community Tips

1. Use microSD cards smaller than 1GB such as 512MB and overwrite the same cards to minimize variations.
2. If the bootloader step is not working, double check the microSD card again for files or folders created by the stock firmware (sometimes if your timing is off with the Setup press the camera will create a time stamp related folder that needs to be deleted before trying again).
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
