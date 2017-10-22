## Installattion of Telnet

1. Go to /system/bin/
2. Copy file "iCamera" to "iCamera.old"
3. Create new File "iCamera" and give it chmod 777:

```
#!/bin/sh
busybox telnetd &
```


## Connect to your network:

Copy following File into /system/dafang/wpa_supplicant.conf
```
ctrl_interface=/var/run/wpa_supplicant
ctrl_interface_group=0
ap_scan=1

network={
        ssid="*****"
        key_mgmt=WPA-PSK
        pairwise=CCMP TKIP
        group=CCMP TKIP WEP104 WEP40
        psk="*****"

        priority=2
}
```
Run following Commands:

```
wpa_supplicant -B -i wlan0 -c /system/dafang/wpa_supplicant.conf -P /var/run/wpa_supplicant.pid
udhcpc -i wlan0 -p /var/run/udhcpc.pid -b

```
