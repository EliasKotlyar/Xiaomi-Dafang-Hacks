#!/bin/sh

echo "Content-type: text/html"
echo ""
source func.cgi
if [ -e "/etc/fang_hacks.cfg" ]; then source /etc/fang_hacks.cfg; fi
PATH="/bin:/sbin:/usr/bin:/system/bin"

CFG_MODE="${NETWORK_MODE:-0}"
CFG_CLIENT="/media/mmcblk0p2/data/etc/wpa_supplicant.conf"
CFG_AP="/media/mmcblk0p2/data/etc/hostapd.conf"
CFG_DHCPD="/media/mmcblk0p2/data/etc/udhcpd.conf"


if [ -n "$F_action" ]; then
  case "$F_action" in
    connect)
      client_ssid=$(printf '%b' "${F_ssid//%/\\x}")
      client_key=$(printf '%b' "${F_key//%/\\x}")
      ACTION_MSG="$(/media/mmcblk0p2/data/etc/scripts/01-network.cgi connect "$client_ssid" "$client_key")"
      ACTION_RC=$?
      CFG_MODE=1
      ;;
    apply)
      ACTION_RC=1
      apply_ssid=$(printf '%b' "${F_ssid//%/\\x}")
      apply_key=$(printf '%b' "${F_key//%/\\x}")
      case "$F_mode" in
        0)
          # apply cloud settings
          if [ -n "$apply_ssid" ] && [ -n "${apply_key}" ]; then
            ACTION_MSG="Updating cloud settings..."
            echo -n "$apply_ssid" > /etc/config/.wifissid
            echo -n "$apply_key" > /etc/config/.wifipasswd
            ACTION_RC=0
            CFG_MODE=0
          fi
          ;;
        1)
          # apply wpa_supplicant settings
          if [ -n "$apply_ssid" ] && [ -n "${apply_key}" ]; then
            if [ -e "$CFG_CLIENT" ]; then
              ACTION_MSG="Updating wpa_supplicant..."
              sed -i.bak 's/^\(\sssid\).*/\1="'"${apply_ssid}"'"/; s/^\(\spsk\).*/\1="'"${apply_key}"'"/' "$CFG_CLIENT" 2>&1
              ACTION_RC=$?
              CFG_MODE=1 
            else
              ACTION_MSG="$CFG_CLIENT doesn't exist!"
            fi
          fi
          ;;
        2)
          # apply hostapd settings
          if [ -n "$apply_ssid" ] && [ -n "$apply_key" ]; then
            if [ -e "$CFG_AP" ]; then
              ACTION_MSG="Updating hostapd..."
              sed -i.bak 's/^\(ssid\).*/\1='"${apply_ssid}"'/; s/^\(wpa_passphrase\).*/\1='"${apply_key}"'/' "$CFG_AP" 2>&1
              ACTION_RC=$?
              CFG_MODE=2
            else
              ACTION_MSG="$CFG_AP doesn't exist!"
            fi
          fi
          ;;
      esac
      if [ $ACTION_RC -eq 0 ]; then
        # apply network.cgi mode
        sed -i.bak 's/^NETWORK_MODE=[0-9]/NETWORK_MODE='$CFG_MODE'/' /etc/fang_hacks.cfg
        ACTION_MSG="$ACTION_MSG<br/>Applying network.cgi mode $CFG_MODE"
        echo "Restarting Network..."
        ACTION_MSG="$ACTION_MSG<br/><pre>$(/media/mmcblk0p2/data/etc/scripts/01-network.cgi start 2>&1)</pre>"
      fi
      ;;
  esac
fi

if [ -e "$CFG_CLIENT" ]; then
    CFG_SSID="$(cat "$CFG_CLIENT")"
fi

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
span.label { font-weight: bold; display: inline-block; }
span.error { font-weight: bold; color: red; display; inline-block; }
legend { font-size: 12 }
</style>

<script>
function updatePanel() {
  if (document.getElementById('mode_cloud').checked) {
    document.getElementById('cloud-pnl').style.display = 'block';
    document.getElementById('client-pnl').style.display = 'none';
    document.getElementById('ap-pnl').style.display = 'none';
  } else if (document.getElementById('mode_client').checked) {
    document.getElementById('cloud-pnl').style.display = 'none';                                                      
    document.getElementById('client-pnl').style.display = 'block';                                                      
    document.getElementById('ap-pnl').style.display = 'none';
    if ("$ACTION_RC" == "0") {
      // connect success, allow apply
      document.getElementById('btn_apply').disabled = false;
    } else {
      document.getElementById('btn_apply').disabled = true;
    }
  } else if (document.getElementById('mode_ap').checked) {                 
    document.getElementById('cloud-pnl').style.display = 'none';          
    document.getElementById('client-pnl').style.display = 'none';              
    document.getElementById('ap-pnl').style.display = 'block';
    document.getElementById('btn_apply').disabled = false;
  }
}

function updateNetworkDetails() {
  var e = document.getElementById('network-list');
  var ssid = e.options[e.selectedIndex].text;
  var addr = document.getElementById(ssid + '_ADDR').value;
  var enc = document.getElementById(ssid + '_ENC').value;
  var qual = document.getElementById(ssid + '_QUAL').value;
  document.getElementById('ssid_name').textContent = ssid;
  document.getElementById('ssid_addr').textContent = addr;
  document.getElementById('ssid_signal').textContent = qual + '%';
  document.getElementById('ssid_encryption').textContent = enc;
  document.getElementById('network-details').style.display = 'block';
  document.getElementById('btn_connect').disabled = false;
  document.getElementById('btn_apply').disabled = true;
  document.getElementById('ssid_key').value = "";
}

function postData(to, p) {
  var myForm = document.createElement("form");
  myForm.method="post";
  myForm.action = to;
  for (var k in p) {
    var myInput = document.createElement("input") ;
    myInput.setAttribute("name", k) ;
    myInput.setAttribute("value", p[k]);
    myForm.appendChild(myInput) ;
  }
  document.body.appendChild(myForm);
  myForm.submit();
  document.body.removeChild(myForm);
}

function apply_config() {
  if (document.getElementById('mode_cloud').checked) {
    var data = {
      action: 'apply',
      mode: 0,
      ssid: document.getElementById('cloud_ssid').value,
      key: document.getElementById('cloud_key').value
    };
    postData('/cgi-bin/network', data);
  } else if (document.getElementById('mode_client').checked) {
    var data = {
      action: 'apply',
      mode: 1,
      ssid: document.getElementById('ssid_name').textContent,
      key: document.getElementById('ssid_key').value
    };
    if (data['key'].length >= 8 && data['key'].length <= 63) {
      postData('/cgi-bin/network', data);
    } else {
      alert("Passphrase must be between 8 and 63 chars!");
    }
  } else if (document.getElementById('mode_ap').checked) {
    var data = {
      action: 'apply',
      mode: 2,
      ssid: document.getElementById('ap_ssid').value,
      key: document.getElementById('ap_key').value
    };
    var addr = document.getElementById('ap_addr').value;
    var msg = [
      "A HotSpot named '" + data['ssid'] + "' will be created.",
      "To continue using the device, you will first need to connect to it.",
      "Once connected the status page can be accessed on:",
      "",
      "http://" + addr + "/cgi-bin/status",
      "",
      "Are you sure?"
    ].join("\n");
    if (confirm(msg) != true) {
      data = null;
    }
  }
  if (typeof data !== 'undefined' && data) {
    if (data['key'].length >= 8 && data['key'].length <= 63) {
      postData('/cgi-bin/network', data);
    } else {
      alert("Passphrase must be between 8 and 63 chars!");
    }
  }
}

function connect_ssid() {
  var ssid = document.getElementById('ssid_name').textContent;
  var enc = document.getElementById(ssid + '_ENC').value;
  if (enc != "WPA") { alert("Sorry, " + enc + " encryption is not supported!"); return; }
  var data = {
    action: 'connect',
    ssid: ssid,
    key: document.getElementById('ssid_key').value
  };
  if (data['key'].length >= 8 && data['key'].length <= 63) {
    postData('/cgi-bin/network', data);
  } else {
    alert("Passphrase must be between 8 and 63 chars!");
  }
}

function onLoad() {
    var id = $(case $CFG_MODE in
                0) echo -n \'mode_cloud\' ;;
                1) echo -n \'mode_client\' ;;
                2) echo -n \'mode_ap\' ;;
             esac);
    document.getElementById(id).checked = true;
EOF
  if [ "$ACTION_RC" == 0 ]; then
    if [ "$F_action" == "connect" ]; then
      echo "document.getElementById('network.cgi-list').value = \"$client_ssid\";"
      echo "updateNetworkDetails();"
      echo "document.getElementById('ssid_key').value = \"$client_key\";"
    fi
  fi
cat << EOF
    updatePanel();
}

window.onload = onLoad;
</script>
</head>
<body>
<h1>Network Settings</h1>
<hr/>
<button title='Status page' type='button' onClick="window.location.href='status.cgi'">Status</button>
<button title='Reboot the device' type='button' onClick="window.location.href='action.cgi?cmd=reboot'">Reboot</button>
<button title='Info' type='button' onClick="window.location.href='scripts.cgi'">Scripts</button>
<button title='View /tmp/hacks.log' type='button' onClick="window.location.href='action.cgi?cmd=showlog'">View log</button>
<!-- <hr/>
<div style='clear: both;'><pre>$ACTION_MSG</pre></div>
<div style='clear: both;'>
<fieldset style='display: inline-block;'>
<legend>Wireless Mode</legend>
<input style='' onClick='updatePanel()' type='radio' name='mode' id='mode_cloud' value='mode_cloud'/>
<label for='mode_cloud'>Cloud</label>
<input style='' onClick='updatePanel()' type='radio' name='mode' id='mode_client' value='mode_client'/>
<label for='mode_cloud'>Wireless Client</label>
<input style='' onClick='updatePanel()' type='radio' name='mode' id='mode_ap' value='mode_ap'/>
<label for='mode_ap'>Access Point</label>
</fieldset>
<br/>

<div id='client-pnl' style='display: none'>
<fieldset style='display: inline-block'>
<legend>Wireless Client</legend>
EOF
SSID="$(iwconfig wlan0 | grep ESSID | cut -d\" -f2)"
AP="$(iwconfig | grep -o "Access Point:.*" | grep -E -o "([0-9A-F]{2}:){5}[0-9A-F]{2}")"
if [ -n "$SSID" ]; then
  echo "Connected to: $SSID<br/>"
  echo "Access Point: $AP<br/>"
  echo "<hr/>"
fi
echo "<div style='float: left'>"
echo "<form name='network.cgi-info'>"
echo "Select Access Point:<br/>"
echo "<select id='network.cgi-list' size='5' onChange='updateNetworkDetails()' style='width: 20em'>"
echo "<option value='' disabled selected style='display:none;'>Label</option>"

hidden=""
while read -r x; do
  SSID=$(echo "$x" | cut -f1)
  ADDR=$(echo "$x" | cut -f2)
  ENC=$(echo "$x" | cut -f3)
  QUAL=$(echo "$x" | cut -f4)
  echo "<option id=\"${SSID}_OPT\">$SSID</option>"
  hidden="$hidden 
         <input type='hidden' id=\"${SSID}_QUAL\" value=\"$QUAL\"/> 
         <input type='hidden' id=\"${SSID}_ENC\" value=\"$ENC\"/>
         <input type='hidden' id=\"${SSID}_ADDR\" value=\"$ADDR\"/>"

done <<EOT
$(iwlist wlan0 scan 2>/dev/null | /system/sdcard/scripts/iwlist.awk | /system/sdcard/bin/busybox sort -rgk4)
EOT
echo "</select>"
echo "$hidden"
echo "</form>"

cat << EOF
</div>
<div id='network-details' style='float: left; padding: 0.5em; line-height: 1.5em; display: none'>
<span class='label' style='width: 5em'>Name:</span><span id='ssid_name'></span><br/>
<span class='label' style='width: 5em'>Address:</span><span id='ssid_addr'></span><br/>
<span class='label' style='width: 5em'>Signal:</span><span id='ssid_signal'></span><br/>
<span class='label' style='width: 5em'>Security:</span><span id='ssid_encryption'></span><br/>
</div>
<div style='clear: both'>
Passphrase:
<input type='text' id='ssid_key'/>
<button type='button' disabled id='btn_connect' title='Connect'
  onClick='connect_ssid()'>Connect</button>
</div>
<div style='clear: both'/>
</fieldset>
</div> <!-- client-pnl -->

<div id='cloud-pnl' style='display: none'>
<fieldset style='display: inline-block'>
<legend>Cloud Mode</legend>
In this mode, network is managed by cloud apps.<br/>
A reboot is required to re-connect after settings are changed!<br/>
EOF
if [ "$DISABLE_CLOUD" -eq 1 ]; then
  echo "<span class='error'>"
  echo "Warning: Cloud apps are disabled!<br/>"
  echo "If you apply this mode network.cgi will NOT be initialized after reboot!"
  echo "</span>"
fi
echo "<hr/> "

echo "<div style='float: left'>"
echo "<form name='network.cgi-info'>"
echo "Cloud WiFi Settings:<br/>"
echo "<label for='cloud_ssid' style='display: inline-block; width: 8em'>Network SSID:</label>"
echo "<input id='cloud_ssid' value='$(cat /etc/config/.wifissid)' type='text'/><br/>"
echo "<label for='cloud_key' style='display: inline-block; width: 8em'>Passphrase:</label>"
echo "<input id='cloud_key' value='$(cat /etc/config/.wifipasswd)' type='text'/>"
echo "</form></div>"
cat << EOF
</fieldset>
</div> <!-- cloud-pnl -->
<div id='ap-pnl' style='display: none'>
<fieldset style='display: inline-block'>
<legend>Access Point</legend>
Create a Wireless Hotspot.<br/>
EOF
echo "<hr/>"
ap_addr="$(grep "^opt.*router" $CFG_DHCPD | awk '{print $3}')"
ap_ssid="$(grep "^ssid=" $CFG_AP | cut -d'=' -f2)"
ap_key="$(grep "^wpa_passphrase=" $CFG_AP | cut -d'=' -f2)"
echo "<div style='float: left'>"
echo "<form name='network.cgi-info'>"
echo "Hotspot settings:<br/>"
echo "<label for='ap_addr' style='display: inline-block; width: 8em'>IP Address:</label>"
echo "<input id='ap_addr' value='$ap_addr' type='text' disabled title='You must manually edit configs to change addressing!'/><br/>"
echo "<label for='ap_ssid' style='display: inline-block; width: 8em'>Network SSID:</label>"
echo "<input id='ap_ssid' value='$ap_ssid' type='text'/><br/>"
echo "<label for='ap_key' style='display: inline-block; width: 8em'>Passphrase:</label>"
echo "<input id='ap_key' value='$ap_key' type='text'/><br/>"
echo "</form></div>"

cat << EOF
</fieldset>
</div> <!-- ap-pnl -->
<hr/>
<button type='button' id='btn_apply' disabled onClick="apply_config()">Apply</button>
<hr/> -->
Information:
<pre>Interfaces:<br/>$(ifconfig; iwconfig)</pre>
<pre>Routes:<br/>$(route)</pre>
<pre>DNS:<br/>$(cat /etc/resolv.conf)</pre>
</body>
</html>
EOF


