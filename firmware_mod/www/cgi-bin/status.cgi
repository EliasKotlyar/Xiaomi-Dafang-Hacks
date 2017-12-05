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
<div style="font-family: monospace, fixed; font-weight: bold;">
<span style=";color:#55f">____</span><span>&#160;&#160;</span><span style=";color:#55f">__.__</span><span>&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;</span><span style=";color:#00a">________</span><span style=";color:#aaa">___</span><span>&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;</span><br />
<span style=";color:#55f">\</span><span>&#160;&#160;&#160;</span><span style=";color:#55f">\/</span><span>&#160;&#160;</span><span style=";color:#00a">|_______</span><span>&#160;&#160;&#160;&#160;</span><span style=";color:#00a">____</span><span style=";color:#aaa">\_</span><span>&#160;&#160;&#160;</span><span style=";color:#aaa">__________</span><span>&#160;&#160;&#160;&#160;</span><span style=";color:#555">____</span><span>&#160;&#160;&#160;</span><span style=";color:#555">____</span><span>&#160;&#160;</span><br />
<span>&#160;</span><span style=";color:#00a">\</span><span>&#160;&#160;&#160;&#160;&#160;</span><span style=";color:#00a">/|</span><span>&#160;&#160;</span><span style=";color:#00a">\__</span><span>&#160;&#160;</span><span style=";color:#aaa">\</span><span>&#160;&#160;</span><span style=";color:#aaa">/</span><span>&#160;&#160;</span><span style=";color:#aaa">_</span><span>&#160;</span><span style=";color:#aaa">\|</span><span>&#160;&#160;&#160;&#160;</span><span style=";color:#aaa">__</span><span style=";color:#555">)</span><span>&#160;</span><span style=";color:#555">\__</span><span>&#160;&#160;</span><span style=";color:#555">\</span><span>&#160;&#160;</span><span style=";color:#555">/</span><span>&#160;&#160;&#160;&#160;</span><span style=";color:#555">\</span><span>&#160;</span><span style=";color:#55f">/</span><span>&#160;</span><span style=";color:#55f">___\</span><span>&#160;</span><br />
<span>&#160;</span><span style=";color:#00a">/</span><span>&#160;&#160;&#160;&#160;&#160;</span><span style=";color:#00a">\</span><span style=";color:#aaa">|</span><span>&#160;&#160;</span><span style=";color:#aaa">|/</span><span>&#160;</span><span style=";color:#aaa">__</span><span>&#160;</span><span style=";color:#aaa">\(</span><span>&#160;&#160;</span><span style=";color:#aaa">&lt;_&gt;</span><span>&#160;</span><span style=";color:#555">|</span><span>&#160;&#160;&#160;&#160;&#160;</span><span style=";color:#555">\</span><span>&#160;&#160;&#160;</span><span style=";color:#555">/</span><span>&#160;</span><span style=";color:#555">__</span><span>&#160;</span><span style=";color:#55f">\|</span><span>&#160;&#160;&#160;</span><span style=";color:#55f">|</span><span>&#160;&#160;</span><span style=";color:#55f">/</span><span>&#160;</span><span style=";color:#55f">/_/</span><span>&#160;&#160;</span><span style=";color:#55f">&gt;</span><br />
<span style=";color:#aaa">/___/\</span><span>&#160;&#160;</span><span style=";color:#aaa">|__(____</span><span>&#160;&#160;</span><span style=";color:#555">/\____/\___</span><span>&#160;&#160;</span><span style=";color:#555">/</span><span>&#160;&#160;</span><span style=";color:#55f">(____</span><span>&#160;&#160;</span><span style=";color:#55f">|___|</span><span>&#160;&#160;</span><span style=";color:#00a">\___</span><span>&#160;&#160;</span><span style=";color:#00a">/</span><span>&#160;</span><br />
<span>&#160;&#160;&#160;&#160;&#160;&#160;</span><span style=";color:#aaa">\_</span><span style=";color:#555">/</span><span>&#160;&#160;&#160;&#160;&#160;&#160;&#160;</span><span style=";color:#555">\/</span><span>&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;</span><span style=";color:#55f">\/</span><span>&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;</span><span style=";color:#55f">\</span><span style=";color:#00a">/</span><span>&#160;&#160;&#160;&#160;&#160;</span><span style=";color:#00a">\/_____/</span><span>&#160;&#160;</span><br />
</div>
<div style="font-family: monospace, fixed; font-weight: bold;">
<span><pre style="display:inline">               </pre></span><span>&#160;&#160;</span><span style=";color:#55f">___</span><span>&#160;</span><span style=";color:#55f">___</span><span>&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;</span><span style=";color:#00a">__</span><span>&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;</span><br />
<span><pre style="display:inline">               </pre></span><span>&#160;</span><span style=";color:#55f">/</span><span>&#160;&#160;&#160;</span><span style=";color:#55f">|</span><span>&#160;&#160;&#160;</span><span style=";color:#00a">\_____</span><span>&#160;&#160;&#160;&#160;</span><span style=";color:#00a">____</span><span>&#160;</span><span style=";color:#aaa">|</span><span>&#160;&#160;</span><span style=";color:#aaa">|</span><span>&#160;</span><span style=";color:#aaa">__</span><span>&#160;</span><span style=";color:#aaa">______</span><br />
<span><pre style="display:inline">               </pre></span><span style=";color:#00a">/</span><span>&#160;&#160;&#160;&#160;</span><span style=";color:#00a">~</span><span>&#160;&#160;&#160;&#160;</span><span style=";color:#00a">\__</span><span>&#160;&#160;</span><span style=";color:#00a">\</span><span>&#160;</span><span style=";color:#aaa">_/</span><span>&#160;</span><span style=";color:#aaa">___\|</span><span>&#160;&#160;</span><span style=";color:#aaa">|/</span><span>&#160;</span><span style=";color:#aaa">//</span><span>&#160;&#160;</span><span style=";color:#555">___/</span><br />
<span><pre style="display:inline">               </pre></span><span style=";color:#00a">\</span><span>&#160;&#160;&#160;&#160;</span><span style=";color:#00a">Y</span><span>&#160;&#160;&#160;&#160;</span><span style=";color:#aaa">//</span><span>&#160;</span><span style=";color:#aaa">__</span><span>&#160;</span><span style=";color:#aaa">&#92;&#92;</span><span>&#160;&#160;</span><span style=";color:#aaa">\___</span><span style=";color:#555">|</span><span>&#160;&#160;&#160;&#160;</span><span style=";color:#555">&lt;</span><span>&#160;</span><span style=";color:#555">\___</span><span>&#160;</span><span style=";color:#555">\</span><span>&#160;</span><br />
<span><pre style="display:inline">               </pre></span><span>&#160;</span><span style=";color:#aaa">\___|_</span><span>&#160;&#160;</span><span style=";color:#aaa">/(____</span><span>&#160;&#160;</span><span style=";color:#555">/\___</span><span>&#160;&#160;</span><span style=";color:#555">|__|_</span><span>&#160;</span><span style=";color:#555">/_</span><span style=";color:#55f">___</span><span>&#160;&#160;</span><span style=";color:#55f">&gt;</span><br />
<span><pre style="display:inline">               </pre></span><span>&#160;&#160;&#160;&#160;&#160;&#160;&#160;</span><span style=";color:#aaa">\</span><span style=";color:#555">/</span><span>&#160;&#160;&#160;&#160;&#160;&#160;</span><span style=";color:#555">\/</span><span>&#160;&#160;&#160;&#160;&#160;</span><span style=";color:#555">\/</span><span>&#160;&#160;&#160;&#160;&#160;</span><span style=";color:#55f">\/</span><span>&#160;&#160;&#160;&#160;</span><span style=";color:#55f">\/</span><span>&#160;</span><br />
<span><pre style="display:inline">                                              Version 0.2.0</pre></span>
<br/>
<br/>
</div>
EOF

cat << EOF
</p>
<hr/>
<button title='Reboot the device' type='button' onClick="window.location.href='action.cgi?cmd=reboot'">Reboot</button>
<button title='Manage scripts' type='button' onClick="window.location.href='scripts'">Manage scripts</button>
<button title='Network' type='button' onClick="window.location.href='network'">Network</button>
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
<tr>
  <th>Process list:</th>
  <td><pre>$(ps)</td>
</tr>
<tr>
  <th>Mounts:</th>
  <td><pre>$(mount)</td>
</tr>

<tr>
  <th>Blue LED:</th>
  <td>
  <button title='' type='button' onClick="window.location.href='action.cgi?cmd=blue_led_on'">On</button>
  <button title='' type='button' onClick="window.location.href='action.cgi?cmd=blue_led_off'">Off</button>
  </td>
</tr>
<tr>
  <th>Yellow LED:</th>
  <td>
  <button title='' type='button' onClick="window.location.href='action.cgi?cmd=yellow_led_on'">On</button>
  <button title='' type='button' onClick="window.location.href='action.cgi?cmd=yellow_led_off'">Off</button>
  </td>
</tr>
<tr>
  <th>IR LED:</th>
  <td>
  <button title='' type='button' onClick="window.location.href='action.cgi?cmd=ir_led_on'">On</button>
  <button title='' type='button' onClick="window.location.href='action.cgi?cmd=ir_led_off'">Off</button>
  </td>
</tr>

<tr>
  <th>Motor:</th>
  <td>
  <button title='' type='button' onClick="window.location.href='action.cgi?cmd=motor_left'">Left</button>
  <button title='' type='button' onClick="window.location.href='action.cgi?cmd=motor_right'">Right</button>
  </td>
</tr>

</table>
</div>
</body>
</html>
EOF
