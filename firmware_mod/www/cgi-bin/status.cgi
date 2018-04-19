#!/bin/sh

echo "Content-type: text/html"
echo ""

cat << EOF
<!DOCTYPE html>
<html>

<head>
    <title>Fang Hacks</title>
    <style type="text/css">
        body { background-color: #B0E0E6; font-family: verdana, sans-serif; }
        .err { color: red; }
        hr { height: 1px; border: 0; border-top: 1px solid #aaa; }
        button, input[type=submit] { background-color: #ddeaff; }
        .tbl { border-collapse: collapse; border-spacing: 0;}
        .tbl th { text-align: left; vertical-align: top; font-weight: bold; padding: 10px 5px; border-style: solid; border-width: 1px; overflow: hidden; word-break: normal; }
        .tbl td { padding: 10px 5px; border-style: solid; border-width: 1px; overflow: hidden; word-break: normal; }
    </style>
</head>

<body>
EOF

source header.cgi

cat << EOF
<br/>
<br/>
</div>
</p>
<hr/>
<button title='Reboot the device' type='button' onClick="window.location.href='cgi-bin/action.cgi?cmd=reboot'">Reboot</button>
<button title='Manage scripts' type='button' onClick="window.location.href='cgi-bin/scripts.cgi'">Manage scripts</button>
<button title='Network' type='button' onClick="window.location.href='cgi-bin/network.cgi'">Network</button>
<button title='View /tmp/hacks.log' type='button' onClick="window.location.href='cgi-bin/action.cgi?cmd=showlog'">View log</button>
<button title='Motion Configuration' type='button' onClick="window.open('/configmotion.html')">ConfigMotion</button>
<button title='live view' type='button' onClick="window.open('/live.html')">Live view</button>
<hr/>
<table class='tbl'>
    <tr>
        <th>Date:</th>
        <td>
            <form style="margin: 0px" action="/cgi-bin/action.cgi?cmd=settz" method="post">
                $(date)
                <label style="margin-left: 1em" for="tz">TZ:</label>
                <input id="tz" name="tz" type="text" size="25" value="$(cat /etc/TZ)" />
				<label  for="ntp_srv">NTP Server:</label>
				<input id="ntp_srv" name="ntp_srv" type="text" size="25" value="$(cat /system/sdcard/config/ntp_srv.conf)"/>
                <label for="hostname">Hostname:</label>
                <input id="hostname" name="hostname" type="text" size="15" value="$(hostname)" />
                <input type="submit" value="Set" />
            </form>
        </td>
    </tr>
    <tr>
        <th>Version:</th>
        <td>$(cut -d'=' -f2 /etc/os-release) </td>
    </tr>


    <script>
        function call(url){
                var xhr = new XMLHttpRequest();
                xhr.open('GET', url, true);
                xhr.send();
        }
    </script>

    <tr>
        <th>Blue LED:</th>
        <td>
            <button title='' type='button' onClick="call('action.cgi?cmd=blue_led_on')">On</button>
            <button title='' type='button' onClick="call('action.cgi?cmd=blue_led_off')">Off</button>
        </td>
    </tr>
    <tr>
        <th>Yellow LED:</th>
        <td>
            <button title='' type='button' onClick="call('action.cgi?cmd=yellow_led_on')">On</button>
            <button title='' type='button' onClick="call('action.cgi?cmd=yellow_led_off')">Off</button>
        </td>
    </tr>
    <tr>
        <th>IR LED:</th>
        <td>
            <button title='' type='button' onClick="call('action.cgi?cmd=ir_led_on')">On</button>
            <button title='' type='button' onClick="call('action.cgi?cmd=ir_led_off')">Off</button>
        </td>
    </tr>
    <tr>
        <th>IR Cut:</th>
        <td>
            <button title='' type='button' onClick="call('action.cgi?cmd=ir_cut_on')">On</button>
            <button title='' type='button' onClick="call('action.cgi?cmd=ir_cut_off')">Off</button>
        </td>
    </tr>
    <tr>
        <th>Auto Night Mode:</th>
        <td>
            <button title='' type='button' onClick="call('action.cgi?cmd=auto_night_mode_start')">On</button>
            <button title='' type='button' onClick="call('action.cgi?cmd=auto_night_mode_stop')">Off</button>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
            Use average measurement on switching. Number of measurements: <form style="display: inline;" action="/cgi-bin/action.cgi?cmd=setldravg" method="post">
                <select name="avg">
    <option value="1" $(if [ "$(sed s/AVG=// /system/sdcard/config/ldr-average)" -eq 1 ]; then echo selected; fi)>1</option>
    <option value="2" $(if [ "$(sed s/AVG=// /system/sdcard/config/ldr-average)" -eq 2 ]; then echo selected; fi)>2</option>
    <option value="3" $(if [ "$(sed s/AVG=// /system/sdcard/config/ldr-average)" -eq 3 ]; then echo selected; fi)>3</option>
    <option value="4" $(if [ "$(sed s/AVG=// /system/sdcard/config/ldr-average)" -eq 4 ]; then echo selected; fi)>4</option>
    <option value="5" $(if [ "$(sed s/AVG=// /system/sdcard/config/ldr-average)" -eq 5 ]; then echo selected; fi)>5</option>
    <option value="10" $(if [ "$(sed s/AVG=// /system/sdcard/config/ldr-average)" -eq 10 ]; then echo selected; fi)>10</option>
    <option value="15" $(if [ "$(sed s/AVG=// /system/sdcard/config/ldr-average)" -eq 15 ]; then echo selected; fi)>15</option>
  </select>
                <input type="submit" value="Set" /> </form>
        </td>
    </tr>
    <tr>
        <th>RTSP-Server Nightvision</th>
        <td>
            <button title='' type='button' onClick="call('action.cgi?cmd=toggle-rtsp-nightvision-on')">On</button>
            <button title='' type='button' onClick="call('action.cgi?cmd=toggle-rtsp-nightvision-off')">Off</button>
        </td>
    </tr>
    <tr>
        <th>RTSP-Flip</th>
        <td>
            <button title='' type='button' onClick="call('action.cgi?cmd=flip-on')">On</button>
            <button title='' type='button' onClick="call('action.cgi?cmd=flip-off')">Off</button>
        </td>
    </tr>

    <tr>
        <th>Motor:</th>
        <td>
            &nbsp;&nbsp;&nbsp;&nbsp;<button title="" type="button" onclick="call('action.cgi?cmd=motor_up&val='+document.getElementById('val').value)">&nbsp;Up&nbsp;</button>
            <br>
            <button title="" type="button" onclick="call('action.cgi?cmd=motor_left&val='+document.getElementById('val').value)">Left</button>&nbsp;
            <button title="" type="button" onclick="call('action.cgi?cmd=motor_right&val='+document.getElementById('val').value)">Right</button>
            <br> &nbsp;&nbsp;&nbsp;
            <button title="" type="button" onclick="call('action.cgi?cmd=motor_down&val='+document.getElementById('val').value)">Down</button> &nbsp;&nbsp;&nbsp;
            <input type="text" id="val" name="val" value="100">
            <button title='' type='button' onClick="call('action.cgi?cmd=motor_vcalibrate')">Calibrate Vertical</button>
            <button title='' type='button' onClick="call('action.cgi?cmd=motor_hcalibrate')">Calibrate Horizontal</button>
        </td>

    </tr>

    <tr>
        <th>Audio:</th>
        <td>
            <button title='' type='button' onClick="call('action.cgi?cmd=audio_test')">Test</button>
        </td>
    </tr>

    <tr>
        <th>Get Image</th>
        <td>
            <a href='currentpic.cgi' target='_blank'><button title='' type='button' onClick="">Get</button></a></br>

        </td>
    </tr>

<tr>
  <th>Resolution</th>
  <td>
  <form style="margin: 0px" action="/cgi-bin/action.cgi?cmd=setvideosize" method="post">
   Select video size: <select name="video_size">                                                                                              
  <option value="-W 640 -H 360" $(if [ "$(cat /system/sdcard/config/video_size.conf | grep 640)" != "" ]; then echo selected; fi)>640x360</option>
  <option value="-W 1280 -H 720" $(if [ "$(cat /system/sdcard/config/video_size.conf | grep 1280)" != "" ]; then echo selected; fi)>1280x720</option>
  <option value="-W 1600 -H 900" $(if [ "$(cat /system/sdcard/config/video_size.conf | grep 1600)" != "" ]; then echo selected; fi)>1600x900</option>  
  <option value="-W 1920 -H 1080" $(if [ "$(cat /system/sdcard/config/video_size.conf | grep 1920)" != "" ]; then echo selected; fi)>1920x1080</option>
  </select>                                                                                                                                
  <input type="submit" value="Set" /> 
  </form>
  </td>
</tr>
	
    <tr>
        <th>Start H264 RTSP</th>
        <td>
            <button title='' type='button' onClick="call('action.cgi?cmd=h264_start')">Start</button>
            <button title='' type='button' onClick="call('action.cgi?cmd=rtsp_stop')">Stop</button>
            <br>
EOF

PATH="/bin:/sbin:/usr/bin:/media/mmcblk0p2/data/bin:/media/mmcblk0p2/data/sbin:/media/mmcblk0p2/data/usr/bin"

IP=$(ifconfig wlan0 |grep "inet addr" |awk '{print $2}' |awk -F: '{print $2}')
echo "Path to feed : <a href='rtsp://$IP:8554/unicast'>rtsp://$IP:8554/unicast</a></br>"
echo "HLS : <a href='http://$IP:8554/unicast.m3u8'>http://$IP:8554/unicast.m3u8</a></br>"
echo "MPEG-DASH : <a href='http://$IP:8554/unicast.mpd'>http://$IP:8554/unicast.mpd</a></br>"

cat << EOF
</td>
</tr>

<tr>
    <th>Start MJPEG RTSP</th>
    <td>
        <button title='' type='button' onClick="call('action.cgi?cmd=mjpeg_start')">Start</button>
        <button title='' type='button' onClick="call('action.cgi?cmd=rtsp_stop')">Stop</button>
        <br>
EOF

PATH="/bin:/sbin:/usr/bin:/media/mmcblk0p2/data/bin:/media/mmcblk0p2/data/sbin:/media/mmcblk0p2/data/usr/bin"

IP=$(ifconfig wlan0 |grep "inet addr" |awk '{print $2}' |awk -F: '{print $2}')
echo "Path to feed : <a href='rtsp://$IP:8554/unicast'>rtsp://$IP:8554/unicast</a></br>"

cat << EOF
</td>
</tr>
<tr>
    <th>OSD-Display</th>
    <td>
        <form style="margin: 0px" action="/cgi-bin/action.cgi?cmd=osd" method="post">
            <input type="checkbox" name="OSDenable" value="enabled" $(if [ -f /system/sdcard/config/osd ]; then echo checked; fi)> Enable
            Text: <input id="osdtext" name="osdtext" type="text" size="25" value="$(source /system/sdcard/config/osd && echo "$OSD")"/>
            (Enter time-variables in <a href="http://strftime.org/" target="_blank">strftime</a> format)
            <br>
            Osd color <select name="color">
  <option value="0" $(if [ "$(grep COLOR /system/sdcard/config/osd | sed s/COLOR=//)" -eq 0 ]; then echo selected; fi)>White</option>
  <option value="1" $(if [ "$(grep COLOR /system/sdcard/config/osd | sed s/COLOR=//)" -eq 1 ]; then echo selected; fi)>Black</option>
  <option value="2" $(if [ "$(grep COLOR /system/sdcard/config/osd | sed s/COLOR=//)" -eq 2 ]; then echo selected; fi)>Red</option>
  <option value="3" $(if [ "$(grep COLOR /system/sdcard/config/osd | sed s/COLOR=//)" -eq 3 ]; then echo selected; fi)>Green</option>
  <option value="4" $(if [ "$(grep COLOR /system/sdcard/config/osd | sed s/COLOR=//)" -eq 4 ]; then echo selected; fi)>Blue</option>
  <option value="5" $(if [ "$(grep COLOR /system/sdcard/config/osd | sed s/COLOR=//)" -eq 5 ]; then echo selected; fi)>Cyan</option>
  <option value="6" $(if [ "$(grep COLOR /system/sdcard/config/osd | sed s/COLOR=//)" -eq 6 ]; then echo selected; fi)>Yellow</option>
  <option value="7" $(if [ "$(grep COLOR /system/sdcard/config/osd | sed s/COLOR=//)" -eq 7 ]; then echo selected; fi)>Purple</option>
  </select> OSD text size <select name="size">
  <option value="0" $(if [ "$(grep SIZE /system/sdcard/config/osd | sed s/SIZE=//)" -eq 0 ]; then echo selected; fi)>Small</option>
  <option value="1" $(if [ "$(grep SIZE /system/sdcard/config/osd | sed s/SIZE=//)" -eq 1 ]; then echo selected; fi)>Bigger</option>
  </select> Y position <input id="posy" name="posy" type="number" size="6" value="$(source /system/sdcard/config/osd && echo "$POSY")"/>
  Pixels between chars (can be negative)<input id="spacepixels" name="spacepixels" type="number" size="4" value="$(source /system/sdcard/config/osd && echo "$SPACE")"/>
  Fixed width <select name="fixedw">
  <option value="0" $(if [ "$(grep FIXEDW /system/sdcard/config/osd | sed s/FIXEDW=//)" -eq 0 ]; then echo selected; fi)>No</option>
  <option value="1" $(if [ "$(grep FIXEDW /system/sdcard/config/osd | sed s/FIXEDW=//)" -eq 1 ]; then echo selected; fi)>Yes</option>
  </select>
            <BR>
            <BR>
            <input type="submit" value=" Set " />

        </form>
    </td>
</tr>
 <tr>
        <th>Display debug info on OSD</th>
        <td>
            <button title='' type='button' onClick="call('/cgi-bin/action.cgi?cmd=onDebug')">On</button>
            <button title='' type='button' onClick="call('/cgi-bin/action.cgi?cmd=offDebug')">Off</button> 
        </td>
    </tr>
<tr>
    <th>Timelapse</th>
    <td>
        <form style="display: inline;" action="/cgi-bin/action.cgi?cmd=conf_timelapse" method="post">
        Interval: <input id="tlinterval" name="tlinterval" type="text" size="5" value="$(source /system/sdcard/config/timelapse.conf && echo "$TIMELAPSE_INTERVAL")"/>seconds,
        Duration: <input id="tlduration" name="tlduration" type="text" size="5" value="$(source /system/sdcard/config/timelapse.conf && echo "$TIMELAPSE_DURATION")"/>minutes (set to 0 for unlimited)
        <input type="submit" value="Set" />
    </td>
</tr>
<tr>
    <th>Start original Xiaomi Software:</th>
    <td>
        <button title='' type='button' onClick="call('action.cgi?cmd=xiaomi_start')">Start</button>
    </td>
</tr>

<tr>
    <th>Process list:</th>
    <td>
        <pre>$(ps)</td>
</tr>
<tr>
  <th>Mounts:</th>
  <td><pre>$(mount)</td>
</tr>


</table>
</div>
</body>
</html>
EOF
