## General informations:

The custom firmware (CFW) bootloader will boot from microSD only if a microSD is plugged in and has a "run.sh" file on it. Otherwise it will load the stock firmware from the flash memory.

## Installation of the custom firmware with the microSD bootloader

1. Download [CFW-Binary](/hacks/cfw/cfw-1.1.bin)
2. Format your microSD to FAT. NTFS, EXFAT etc. won't work.
2. Put it to microSD and rename it to "demo.bin". There should be no other files on the microSD! This is really important and it won't work if there are any other files on there.
3. Shutdown the Dafang camera, remove the power cable and plug the microSD into the Dafang
3. Hold the setup button on the Dafang camera
4. Plug in the USB power cable
5. Wait until the firmware has finished flashing (like 5 minutes). Disconnect the power as soon as the base starts moving.
6. Remove the microSD and try to start the Dafang camera
7. You should see the blue led shining up for 5 seconds (not blinking) **before** the base starts moving. If not, something went wrong. You should try another microSD. Start over from step 1.


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

3. Modify the file config/wpa_supplicant.conf on the microSD to match your wifi-settings
4. Insert the microSD and start the camera.

## Updating:

If you already have a current custom firmware with custom bootloader installed, you only need to update the content of the microSD

1. Backup your wpa_config/wpa_supplicant.conf
2. Remove all files from the microSD
3. Put everything from "firmware_mod" folder into the **root** of the microSD
4. Copy the backed up wpa_supplicant.conf from step 1 back into the config folder

## Uninstallation

Remove the "run.sh" file from microSD.

## Features

- SSH-Server with username: root password: ismart12
- FTP-Server with username: root password: ismart12
- Webserver
- Image-Snap functionality: http://dafanghacks/cgi-bin/currentpic.cgi?width=1920&height=1080&nightvision=0
- Fang-Hacks (work in progress): http://dafanghacks/cgi-bin/status.cgi
- Horizontal/vertical motor rotation
- Turn on/off blue/yellow/IR LEDs
- RTSP with mJPEG (low quality):
```
/system/sdcard/bin/mjpegStreamer 10
```
- Local h264 recording:
```
/system/sdcard/bin/h264Snap > /system/sdcard/video.h264
```

- Audio-Test:
```
/system/sdcard/bin/audioplay /usr/share/notify/CN/init_ok.wav
```
