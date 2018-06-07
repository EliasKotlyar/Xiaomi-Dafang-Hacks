## Integration in tinyCam

1. Make sure you have the user 'root' and same password set for both HTTPS and RTSP.
2. Download the [custom_vendors.xml](custom_vendors.xml) configuration file.
3. Open tinyCam and go to settings -> Developer Settings -> Custom brand XML file -> Choose custom_vendors.xml
4. Restart tinyCam
5. Run tinyCam and select Brand -> XiaomiHacks and Model -> Dafang

Note: A Custom_vendors.xml 'file not found' error can happen due to tinyCam not taking the correct path from file manager. Make sure it is not prefixed with document etc.

### tinyCam camera settings (with custom_vendor.xml loaded)

Web port number: 443

Protocol: RTSP over TCP (MPEG/H264/H265)

RTSP port number: 8554

Use HTTPS: ticked

### For audio support add the following to your rtspserver.conf

AUDIOFORMAT=PCMU

AUDIOOUTBR=8000:8000

RTSPH264OPTS="-W1280 -H720 -U root:your_password"
