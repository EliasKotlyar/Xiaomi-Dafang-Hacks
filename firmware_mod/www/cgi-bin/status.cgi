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
<button title='Reboot the device' type='button' onClick="window.location.href='action.cgi?cmd=reboot'">Reboot</button>
<button title='Manage scripts' type='button' onClick="window.location.href='scripts.cgi'">Manage scripts</button>
<button title='Network' type='button' onClick="window.location.href='network.cgi'">Network</button>
<button title='View /tmp/hacks.log' type='button' onClick="window.location.href='action.cgi?cmd=showlog'">View log</button>
<hr/>
<table class='tbl'>
<tr>
  <th>Date:</th>
  <td>
      <form style="margin: 0px" action="/cgi-bin/action.cgi?cmd=settz" method="post">
        $(date)
        <label style="margin-left: 1em" for="tz">TZ:</label>
        <input id="tz" name="tz" type="text" size="25" value="$(cat /etc/TZ)"/>
        <label  for="hostname">Hostname:</label>
        <input id="hostname" name="hostname" type="text" size="15" value="$(hostname)"/>
        <input type="submit" value="Set"/>
      </form>
  </td>
</tr>
<tr>
  <th>Version:</th>
  <td>$(cat /etc/os-release | cut -d'=' -f2)</td>
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
    <option value="1" $(if [ `cat /system/sdcard/config/ldr-average | sed s/AVG=//` -eq 1 ]; then echo selected; fi)>1</option>
    <option value="2" $(if [ `cat /system/sdcard/config/ldr-average | sed s/AVG=//` -eq 2 ]; then echo selected; fi)>2</option>
    <option value="3" $(if [ `cat /system/sdcard/config/ldr-average | sed s/AVG=//` -eq 3 ]; then echo selected; fi)>3</option>
    <option value="4" $(if [ `cat /system/sdcard/config/ldr-average | sed s/AVG=//` -eq 4 ]; then echo selected; fi)>4</option>
	<option value="5" $(if [ `cat /system/sdcard/config/ldr-average | sed s/AVG=//` -eq 5 ]; then echo selected; fi)>5</option>
	<option value="10" $(if [ `cat /system/sdcard/config/ldr-average | sed s/AVG=//` -eq 10 ]; then echo selected; fi)>10</option>
	<option value="15" $(if [ `cat /system/sdcard/config/ldr-average | sed s/AVG=//` -eq 15 ]; then echo selected; fi)>15</option>
  </select>
 <input type="submit" value="Set"/>  </form>	
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
  &nbsp;&nbsp;&nbsp;&nbsp;<button title="" type="button" onclick="call('action.cgi?cmd=motor_up')">&nbsp;Up&nbsp;</button>
  <br>
  <button title="" type="button" onclick="call('action.cgi?cmd=motor_left')">Left</button>&nbsp;
  <button title="" type="button" onclick="call('action.cgi?cmd=motor_right')">Right</button>
  <br>
  &nbsp;&nbsp;&nbsp;<button title="" type="button" onclick="call('action.cgi?cmd=motor_down')">Down</button>

&nbsp;&nbsp;&nbsp;
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
  <th>Start H264 RTSP</th>
  <td>
  <button title='' type='button' onClick="call('action.cgi?cmd=h264_start')">Start</button>
  <button title='' type='button' onClick="call('action.cgi?cmd=rtsp_stop')">Stop</button> 
  <br>
EOF

PATH="/bin:/sbin:/usr/bin:/media/mmcblk0p2/data/bin:/media/mmcblk0p2/data/sbin:/media/mmcblk0p2/data/usr/bin"

IP=$(ifconfig wlan0 |grep "inet addr" |awk '{print $2}' |awk -F: '{print $2}')
echo "Path to feed : <a href='rtsp://$(echo $IP):8554/unicast'>rtsp://$(echo $IP):8554/unicast</a></br>"
echo "HLS : <a href='http://$(echo $IP):8554/unicast.m3u8'>http://$(echo $IP):8554/unicast.m3u8</a></br>"
echo "MPEG-DASH : <a href='http://$(echo $IP):8554/unicast.mpd'>http://$(echo $IP):8554/unicast.mpd</a></br>"
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
echo "Path to feed : <a href='rtsp://$(echo $IP):8554/unicast'>rtsp://$(echo $IP):8554/unicast</a></br>"
cat << EOF


  </td>
</tr>
<tr>
  <th>Start H264 RTSP without segmentation</th>
  <td>
  <button title='' type='button' onClick="call('action.cgi?cmd=h264_noseg_start')">Start</button>
  <button title='' type='button' onClick="call('action.cgi?cmd=rtsp_stop')">Stop</button>
  <br>
EOF

PATH="/bin:/sbin:/usr/bin:/media/mmcblk0p2/data/bin:/media/mmcblk0p2/data/sbin:/media/mmcblk0p2/data/usr/bin"

IP=$(ifconfig wlan0 |grep "inet addr" |awk '{print $2}' |awk -F: '{print $2}')
echo "Path to feed : <a href='rtsp://$(echo $IP):8554/unicast'>rtsp://$(echo $IP):8554/unicast</a></br>"
cat << EOF
</td>

<tr>
  <th>OSD-Display</th>
  <td> 
  <form style="margin: 0px" action="/cgi-bin/action.cgi?cmd=osd" method="post"> 
  <input type="checkbox" name="OSDenable" value="enabled" $(if [ -f /system/sdcard/config/osd ]; then echo checked; fi)> Enable 
  <input type="radio" id="up" name="Position" value="UP"  $(if [ `cat /system/sdcard/config/osd | awk '{print $NF}' | sed -e s/\"//` == "UP" ]; then echo checked; fi)>Up 
  <input type="radio" id="down" name="Position" value="DOWN"  $(if [ `cat /system/sdcard/config/osd | awk '{print $NF}' | sed -e s/\"//` == "DOWN" ]; then echo checked; fi)>Down
  Text: <input id="osdtext" name="osdtext" type="text" size="25" value="$(cat /system/sdcard/config/osd | sed -e s/".*-D "// | sed -e s/" *-d.*$"//)"/>
  <input type="submit" value="Set"/><br>
  Enter time-variables in <a href="http://strftime.org/" target="_blank">strftime</a> format 
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
  <td><pre>$(ps)</td>
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
