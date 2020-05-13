#!/bin/sh
source ./func.cgi

echo "Pragma: no-cache"
echo "Cache-Control: max-age=0, no-store, no-cache"

SCRIPT_HOME="/system/sdcard/controlscripts/"
if [ -n "$F_script" ]; then
  script="${F_script##*/}"
  if [ -e "$SCRIPT_HOME/$script" ]; then
    case "$F_cmd" in
      start)
        echo "Content-type: text/html"
        echo ""

        echo "Running script '$script'..."
        echo "<pre>$("$SCRIPT_HOME/$script" 2>&1)</pre>"
        ;;  
      disable)
        rm "/system/sdcard/config/autostart/$script"
        echo "Content-type: application/json"
        echo ""
        echo "{\"status\": \"ok\"}"
        ;;
      stop)
        echo "Content-type: text/html"
        echo ""
        status='unknown'
        echo "Stopping script '$script'..."
        echo "<pre>"
        "$SCRIPT_HOME/$script" stop 2>&1 && echo "OK" || echo "NOK"
        echo "</pre>"
        ;;
      enable)
        echo "#!/bin/sh" > "/system/sdcard/config/autostart/$script"
        echo "$SCRIPT_HOME$script" >> "/system/sdcard/config/autostart/$script"
        echo "Content-type: application/json"
        echo ""
        echo "{\"status\": \"ok\"}"
        ;;
      view)
        echo "Content-type: text/html"
        echo ""
        echo "Contents of script '$script':"
        echo "<pre>$(cat "$SCRIPT_HOME/$script" 2>&1)</pre>"
        ;;
      *)
        echo "Content-type: text/html"
        echo ""
        echo "<p>Unsupported command '$F_cmd'</p>"
        ;;
    esac
  else
    echo "Content-type: text/html"
    echo ""
    echo "<p>$F_script is not a valid script!</p>"
  fi
  return
fi

echo "Content-type: text/html"
echo ""

if [ ! -d "$SCRIPT_HOME" ]; then
  echo "<p>No scripts.cgi found in $SCRIPT_HOME</p>"
else
  SCRIPTS=$(ls -A "$SCRIPT_HOME")

  for i in $SCRIPTS; do
    # Card - start
    echo "<div class='card script_card'>"
    # Header
    echo "<header class='card-header'><p class='card-header-title'>"
    # echo "<div class='card-content'>"
    if [ -x "$SCRIPT_HOME/$i" ]; then
      if grep -q "^status()" "$SCRIPT_HOME/$i"; then
        status=$("$SCRIPT_HOME/$i" status)
        badgestatus=$status
        if [ $? -eq 0 ]; then
          if [ -n "$status" ]; then
            badge="";
          else
            badge="is-badge-warning";
          fi
        else
          badge="is-badge-danger"
          badgestatus="NOK"
        fi
        echo "<span class='badge $badge' data-badge='$badgestatus'>$i</span>"
      else
        echo "$i"
      fi
      # echo "</div>"
      echo "</p></header>"

      # Footer
      echo "<footer class='card-footer'>"
      echo "<span class='card-footer-item'>"

      # Start / Stop / Run buttons
      echo "<div class='buttons'>"
      if grep -q "^start()" "$SCRIPT_HOME/$i"; then
        echo "<button data-target='cgi-bin/scripts.cgi?cmd=start&script=$i' class='button is-link script_action_start' data-script='$i' "
        if [ ! -z "$status" ]; then
          echo "disabled"
        fi
        echo ">Start</button>"
      else
        echo "<button data-target='cgi-bin/scripts.cgi?cmd=start&script=$i' class='button is-link script_action_start' data-script='$i' "
        echo ">Run</button>"
      fi

      if grep -q "^stop()" "$SCRIPT_HOME/$i"; then
        echo "<button data-target='cgi-bin/scripts.cgi?cmd=stop&script=$i' class='button is-danger script_action_stop' data-script='$i' "
        if [ ! -n "$status" ]; then
          echo "disabled"
        fi
        echo ">Stop</button>"
      fi
      echo "</div>"
      echo "</span>"

      # Autostart Switch
      echo "<span class='card-footer-item'>"
      echo "<input type='checkbox' id='autorun_$i' name='autorun_$i' class='switch is-rtl autostart' data-script='$i' "
        echo " data-unchecked='cgi-bin/scripts.cgi?cmd=disable&script=$i'"
        echo " data-checked='cgi-bin/scripts.cgi?cmd=enable&script=$i'"
      if [ -f "/system/sdcard/config/autostart/$i" ]; then
        echo " checked='checked'"
      fi
      echo "'>"
      echo "<label for='autorun_$i'>Autorun</label>"
      echo "</span>"

      # View link
      echo "<a href='cgi-bin/scripts.cgi?cmd=view&script=$i' class='card-footer-item view_script' data-script="$i">View</a>"
      echo "</footer>"
    fi
    # Card - End
    echo "</div>"
  done
fi

script=$(cat /system/sdcard/www/scripts/scripts.cgi.js)
echo "<script>$script</script>"
