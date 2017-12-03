## General informations:

The CFW will boot only if the SDCard is plugged in and has a "run.sh" file on it. It wont affect the normal firmware in any way.

## Installation of custom Firmware(microsd-bootloader)
1. Download [CFW-Binary](/hacks/cfw/cfw-1.1.bin)
2. Format your microsd to FAT. NTFS,EXFAT etc wont work.
2. Put it to microsd and rename to "demo.bin". There should be no more files in the sdcard! This is really important, and it wont work if there are any other files there.
3. Shutdown the Dafang, remove power cable, and plug the SDCard into the Dafang
3. Hold the Setup-Button on the Dafang
4. Plug in the Power-Cable(USB)
5. Wait until the firmware will flash(like 5 minutes). Disconnect the power as soon as the base starts moving.
6. Remove the SDCard and try to start the Dafang
7. You should see the blue led shining up for 5 seconds(not blinking) **before** the base starts moving. If not, something went wrong. You should try another microsd. Start over from Point1


## Installation of the new Firmware

1. Put everything from "firmware_mod" Folder into the **root** of the microsd

It should look like this:
```
E:/
├── bin
├── config
├── run.sh
├── sample_config
├── scripts
└── www

```

2. Modify the file config/wpa_supplicant.conf on the sdcard, to match your wifi-settings
3. Insert the SDcard and start the camera.


## Uninstallation

Remove the "run.sh" file from microsd.

## Features
- SSH-Server
- FTP-Server
- Webserver

- Image-Snap functionality:

http://IP/cgi-bin/currentpic

-Fang-Hacks(not working correctly for now):

http://IP/cgi-bin/status

