### How does the CFW work?
The CFW consists of two parts:
1. The Custom Firmware, which alters the stock firmware to boot from a Micro SD card and needs to be flashed over the stock firmware. It doesn't contain any custom software, it just allows you to boot from a Micro SD card. This will only need to be done once. 
2. The CFW Files, which contains the custom software. You will have to install them onto your Micro SD card after you complete step 1. You can easily modify the software by editing the files on the Micro SD card.

### Does the CFW contain a RTSP-Server? 
Yes, you can watch it through VLC Player.

### Does the CFW connect to any Xiaomi Servers?
No. It does not connect to anything.

### Does the CFW remove the stock firmware?
No. You can still boot the stock firmware if you remove the Micro SD card.

### Is it possible to run the stock firmware and the CFW at the same time?
No, it's not possible and it's very unlikely that this will change in the future.

### Can I revert the CFW back to stock firmware?
Yes, you can. However there is no need to revert it back. If your Micro SD card does not contain the CFW Files, you will just boot the stock software. If you still want to revert back to a stock firmware just flash the appropriate one for your camera from the firmware_original folder the same way you flashed the custom firmware.

### Is it possible to run the CFW without a Micro SD card?
While it can be done, there will be a lot of trouble in getting it to work and is outside the scope of this project.

### Can I have FullHD resolution?
Yes, but you must [flash a custom bootloader](/hacks/flashinguboot.md) to achieve this.

### Can the camera send a multicast stream?
Yes, uncomment and customize the multicast destination IP and port in /system/sdcard/config/rtspserver.conf and restart.

### Can I use USB ethernet cards?
Yes, just create a usb_eth_driver.conf file in /system/sdcard/config.
```
cp /system/sdcard/config/usb_eth_driver.conf.dist /system/sdcard/config/usb_eth_driver.conf
reboot
```
If this file exists the run.sh won't start the WIFI driver but will instead load the usb ethernet driver. Currently only the asix.ko driver is supported but others can be built.

### Which Features does the CFW contain?
- Full working RTSP with H264/MJPEG. Based on https://github.com/mpromonet/v4l2rtspserver
- SSH-Server(dropbear) with username: root password: ismart12
- FTP-Server(bftpd) with username: root password: ismart12
- Webserver(lighttpd) with username: root password: ismart12
- Image-Snap(Get Jpeg Image) 
- Horizontal/vertical motor rotation / move to center
- Turn on/off blue/yellow/IR LEDs/IR-Cut
- Local h264 recording possible:
```
/system/sdcard/bin/h264Snap > /system/sdcard/video.h264
```
- Audio recording/playing possible:
```
Playing Audio:
/system/sdcard/bin/audioplay /usr/share/notify/CN/init_ok.wav volume

Recording Audio:
/system/sdcard/bin/ossrecord /system/sdcard/test.wav 
```
- Curl
- MQTT
- Telegram

- Any additional software that you may want can be compiled separately, and there is a toolchain available but you will need to do this yourself.

### What if my scripts in config/userscripts/motiondetection are not executed or mqtt/telegram messages/emails are not sent on motion?
Your camera probably runs out of memory when processing the motion event. This is likely in cameras with 64MB e.g. the Xiaofang 1s. Try to [enable some swap memory](https://github.com/EliasKotlyar/Xiaomi-Dafang-Hacks/blob/master/firmware_mod/config/swap.conf.dist#L4) by copying `swap.conf.dist` to `swap.conf` and setting `SWAP=true`.
