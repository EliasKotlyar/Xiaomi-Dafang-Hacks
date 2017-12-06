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
        <input id="hostname" name="hostname" type="text" size="15" value="$(cat /etc/hostname)"/>
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
  <th>Motor:</th>
  <td>
  <button title='' type='button' onClick="call('action.cgi?cmd=motor_left')">Left</button>
  <button title='' type='button' onClick="call('action.cgi?cmd=motor_right')">Right</button>
  <button title='' type='button' onClick="call('action.cgi?cmd=motor_up')">Up</button>
  <button title='' type='button' onClick="call('action.cgi?cmd=motor_down')">Down</button>

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
  <a href='currentpic.cgi?width=1920&height=1080' target='_blank'>Get</a>
  </td>
</tr>


<tr>
  <th>Start RTSP</th>
  <td>
  <button title='' type='button' onClick="call('action.cgi?cmd=rtsp_start')">Start</button>
  <button title='' type='button' onClick="call('action.cgi?cmd=rtsp_stop')">Stop</button>
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
