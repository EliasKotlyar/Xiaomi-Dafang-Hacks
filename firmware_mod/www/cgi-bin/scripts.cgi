#!/bin/sh
echo "Content-type: text/html"
echo ""
source func.cgi

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
    <h1>Boot Scripts</h1>
    <hr/>
    <button title='Status page' type='button' onClick="window.location.href='status.cgi'">Status</button>
    <button title='Reboot the device' type='button' onClick="window.location.href='action.cgi?cmd=reboot'">Reboot</button>
    <button title='Network' type='button' onClick="window.location.href='network.cgi'">Network</button>
    <button title='View /tmp/hacks.log' type='button' onClick="window.location.href='action.cgi?cmd=showlog'">View log</button>
    <hr/>
EOF

SCRIPT_HOME="/system/sdcard/controlscripts/"
if [ -n "$F_script" ]; then
  script="${F_script##*/}"
  if [ -e "$SCRIPT_HOME/$script" ]; then
    case "$F_cmd" in
      start)
        echo "Running script '$script'...<br/>"
        echo "<pre>$("$SCRIPT_HOME/$script" 2>&1)</pre>"
        ;;  
      disable)
        echo "Disable script '$script'...<br/>"
        rm "/system/sdcard/config/autostart/$script"
        ;;
      stop)
        echo "Stop script '$script'...<br/>"
        "$SCRIPT_HOME/$script" stop 2>&1 && echo "OK" || echo "NOK"
        echo "<br/>"
        ;;
      enable)
        echo "Enable script '$script'...<br/>"
        echo "#!/bin/sh" > "/system/sdcard/config/autostart/$script"
        echo "$SCRIPT_HOME$script" >> "/system/sdcard/config/autostart/$script"
        ;;
      view)
        echo "Contents of script '$script':<br/>"
        echo "<pre>$(cat "$SCRIPT_HOME/$script" 2>&1)</pre>"
        ;;
      *)
        echo "Unsupported command '$F_cmd'<br/>"
        ;;
    esac
    echo "<hr/>"
  else
    echo "$F_script is not a valid script!<br/>"
  fi
fi

if [ ! -d "$SCRIPT_HOME" ]; then
  echo "No scripts.cgi found in $SCRIPT_HOME<br/>"
else
  SCRIPTS=$(ls -A "$SCRIPT_HOME")
  echo "<table class='tbl'>"
  echo "<tr><th>Service</th><th>Status</th><th/><th/><th>Autostart</th></tr>"
  for i in $SCRIPTS; do
    echo "<tr>"
    echo "<td>$i</td>"
    if [ -x "$SCRIPT_HOME/$i" ]; then
      if grep -q "^status()" "$SCRIPT_HOME/$i"; then
        status=$("$SCRIPT_HOME/$i" status)
        if [ $? -eq 0 ]; then
          if [ -n "$status" ]; then
            bgcolor="green";
          else 
            bgcolor="orange";
          fi
        else
          bgcolor="red"
          status="NOK"
        fi
        echo "<td bgcolor='$bgcolor'>$status</td>";
      else
        echo "<td/>"
      fi

      if grep -q "^start()" "$SCRIPT_HOME/$i"; then
        if [ -z "$status" ]; then
          echo "<td><button title='Start script' type='button' onClick=\"window.location.href='scripts.cgi?cmd=start&script=$i'\">Start</button</td>"
        else
          echo "<td><button title='Already running' disabled>Start</button>"
        fi
      else
        echo "<td><button title='Run script' type='button' onClick=\"window.location.href='scripts.cgi?cmd=start&script=$i'\">Run</button></td>"
      fi

      if grep -q "^stop()" "$SCRIPT_HOME/$i"; then
        if [ -n "$status" ]; then
          echo "<td><button title='Stop script' type='button' onClick=\"window.location.href='scripts.cgi?cmd=stop&script=$i'\">Stop</button></td>"
        else
          echo "<td><button title='Not running' disabled>Stop</button>"
        fi
      else
        echo "<td></td>"
      fi
    fi
    if [ -f "/system/sdcard/config/autostart/$i" ]; then
      echo "<td><button title='Disable script' type='button' onClick=\"window.location.href='scripts.cgi?cmd=disable&script=$i'\">Disable</button></td>"
    else
      echo "<td><button title='Enable script' type='button' onClick=\"window.location.href='scripts.cgi?cmd=enable&script=$i'\">Enable</button></td>"
    fi
    echo "<td><button title='View script' type='button' onClick=\"window.location.href='scripts.cgi?cmd=view&script=$i'\">View</button></td>"
    echo "</tr>"
  done
  echo "</table>"
fi

cat << EOF
</body>
</html>
EOF
