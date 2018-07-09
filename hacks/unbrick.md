## How to unbrick

You need to open the camera and solder three pads (not too hard).
And you will need a serial (usb) adapter to connect the camera to your pc.

- Follow this steps to connect to the camera via serial connection:  
https://github.com/EliasKotlyar/Xiaomi-Dafang-Hacks/blob/master/hacks/serial.md
- If you are lucky you will see some status lines and a command prompt:
`isvp_t20#`  
If you get the command prompt you can continue and try to re-flash the camera.
- Put [demo_5.5.1.177.bin](https://raw.githubusercontent.com/EliasKotlyar/Xiaomi-Dafang-Hacks/master/firmware_original/demo_5.5.1.177.bin) as `demo.bin` on the sdcard.
- Insert the sdcard and reboot the camera
- Execute the following commands:
```
fatload mmc 0:1 0x80600000 demo.bin 0xa8ffc0 0x40
sf probe
sf update 0x80600000 0x40000 0xa90000
reset
```
- The camera should now boot again
- I recommend flashing the image again with the system updater (hold the setup button, ...)  
You can watch the update working over the serial connection

## Target memory addresses (for advanced users)
```
0x000000000000-0x000000040000 : "boot"
0x000000040000-0x000000240000 : "kernel"
0x000000240000-0x000000590000 : "root"
0x000000590000-0x000000630000 : "driver"
0x000000630000-0x000000ad0000 : "appfs"
0x000000ad0000-0x000000cd0000 : "backupk"
0x000000cd0000-0x000000d70000 : "backupd"
0x000000d70000-0x000000f70000 : "backupa"
0x000000f70000-0x000000fb0000 : "config"
0x000000fb0000-0x000000ff0000 : "para"
0x000000ff0000-0x000001000000 : "flag"
```

## Loading and booting a kernel without flashing (for advanced users)
e.g. https://github.com/EliasKotlyar/Xiaomi-Dafang-Hacks/blob/master/firmware_original/5.5.1.177/kernel.bin
```
fatload mmc 0:1 0x80600000 kernel.bin
bootm 0x80600000
```
