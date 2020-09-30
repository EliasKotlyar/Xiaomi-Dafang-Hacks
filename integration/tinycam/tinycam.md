## Integration in tinyCam
As of tinyCam Version [10.2](https://tinycammonitor.com/changelog.html) a "Xiaomi Dafang" camera has been added, it
includes support for Xiaomi-Dafang-Hacks.

1. Make sure you have the user 'root' and same password set for both HTTPS and RTSP.
2. Open tinyCam and go to Manage Cameras > + > Add IP camera, NVR/DVR
3. Fill out the following settings:
   * Camera Brand: Xiaomi
   * Camera Model: Dafang
   * Hostname/IP address: <IP_address/hostname>
   * RTSP port number: 8554
   * Use HTTPS: selected
   * Username: root
   * Password: ismart12 (we recommend changing the default password)
4. Click Camera Status to verify the settings are correct.
  
#### For audio support add the following to your rtspserver.conf

AUDIOFORMAT=PCMU

AUDIOOUTBR=8000:8000

RTSPOPTS="-W1280 -H720 -U root:your_password"
