## General informations:

The CFW will boot only if the SDCard is plugged in and has a "run.sh" file on it. It wont affect the normal firmware in any way.

## Installation of CFW
1. Download [CFW-Binary](/hacks/cfw/cfw-1.0.bin)
2. Put it to microsd and rename to "demo.bin". There should be no more files in the sdcard! This is really important, and it wont work if there are any other files there.
3. Shutdown the Dafang, remove power cable, and plug the SDCard into the Dafang
3. Hold the Setup-Button on the Dafang
4. Plug in the Power-Cable(USB)
5. Wait for 5 minutes(dont unplug the camera until it will bootup to the normal firmware)
6. Unplug the Camera, put everything from "firmware_mod" Folder into the root of the microsd
7. Modify the file wpa_supplicant.conf from the CFW to match your wifi network.
8. Reboot the Camera - it will boot now into CFW

## Uninstallation

Remove the "run.sh" file from microsd.

## Features
- SSH-Server
- FTP-Server
- Webserver
- Image-Snap functionality.


