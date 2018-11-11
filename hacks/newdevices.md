### Installation on generic T10/T20 Devices

It should be possible to install this hack to any T10 or T20 based devices. If you want to do so, begin with the porting tutorial:

### Porting Tutorial
1. Disassemble the Device and make a lot of photos. 
2. Connect via TTL to the camera. You can use the following blog article as a reference: https://nm-projects.de/2016/12/hacking-digoo-bb-m2-mini-wifi-part-1-identify-the-serial-interface/
3. Get root access: https://github.com/EliasKotlyar/Xiaomi-Dafang-Hacks/blob/master/hacks/getroot.md
4. Dump the firmware:
https://github.com/EliasKotlyar/Xiaomi-Dafang-Hacks/blob/master/hacks/firmware-dump.md
5. Dump a bootlog of your camera
6. Collect all the information together in a github issue in this repository

As soon as we have all the information together, we can hopefully provide a new bootloader for your device, which will boot this hack.
