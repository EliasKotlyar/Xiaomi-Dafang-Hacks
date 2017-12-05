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

1. Download the Repository as Zip-File. Dont try to get it with git if you are on windows!
2. Put everything from "firmware_mod" Folder into the **root** of the microsd

It should look like this:
```
E:/
├── bin
├── config
├── run.sh
├── scripts
└── www

```

3. Modify the file config/wpa_supplicant.conf on the sdcard, to match your wifi-settings
4. Insert the SDcard and start the camera.
## Updating:

You just need to update the content of the sdcard if you have already the right firmware installed.

1. Backup the wpa_config/wpa_supplicant.conf
2. Remove all files from the microsd
3. Put everything from "firmware_mod" Folder into the **root** of the microsd
4. Copy the the wpa_supplicant.conf from step 1 to the config folder

## Uninstllation

Remove the "run.sh" file from microsd.

## Features
- SSH-Server
- FTP-Server
- Webserver
- Image-Snap functionality
- Fang-Hacks(not working correctly for now):
- Horizontal Motor rotation
- Turn on/off LEDs
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