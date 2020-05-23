#!/bin/sh

source /system/sdcard/scripts/common_functions.sh

echo "Content-type: text/html"
echo "Pragma: no-cache"
echo "Cache-Control: max-age=0, no-store, no-cache"
echo ""

mount|grep "/system/sdcard"|grep "rw,">/dev/null

if [ $? == 1 ]; then

cat << EOF
  <!-- sdcard warning -->
  <article class="message is-warning">
    <div class="message-header">
      <p>Warning</p>
      <button class="delete" aria-label="delete"></button>
    </div>
    <div class="message-body">
      Your sdcard is mounted read-only. Settings can't be saved.
      <br>
      <p>Please try rebooting. If the problem persists, please <a target="_blank" href="https://github.com/EliasKotlyar/Xiaomi-Dafang-Hacks/search?q=read+only+sdcard&type=Issues">search
      for possible solutions.</a></p>
    </div>
  </article>
  <!-- end sdcard warning -->
EOF

fi

cat << EOF
<!-- System -->
<div class='card status_card'>
    <header class='card-header'><p class='card-header-title'>System</p></header>
    <div class='card-content'>
        <div class='content'>
            <table>
              <tbody>
                <tr>
                  <td> Hostname </td>
                  <td> $(hostname) </td>
                </tr>
                <tr>
                  <td> Model </td>
                  <td> $(detect_model) </td>
                </tr>
                <tr>
                  <td> Firmware date </td>
                  <td> $(if [ -s "/system/sdcard/VERSION" ]; then /system/sdcard/bin/jq -r .date /system/sdcard/VERSION; else echo "Never updated. Make an update to get version."; fi) </td>
                </tr>
                <tr>
                  <td> Firmware branch </td>
                  <td> $(if [ -s "/system/sdcard/VERSION" ]; then /system/sdcard/bin/jq -r .branch /system/sdcard/VERSION; else echo "Never updated. Make an update to get version."; fi) </td>
                </tr>
                <tr>
                  <td> Firmware commit </td>
                  <td> $(if [ -s "/system/sdcard/VERSION" ]; then echo $(check_commit); else echo "Never updated through UI, please run update to get a version file."; fi) </td>
                </tr>
                
                <tr>
                  <td> Kernel Version </td>
                  <td> $(/system/sdcard/bin/busybox uname -v) </td>
                </tr>
                <tr>
                  <td> Bootloader Version </td>
                  <td> $(busybox strings /dev/mtd0 | grep "U-Boot 2") </td>
                <tr>
                <tr>
                  <td> Local Time </td>
                  <td> $(date) </td>
                </tr>
                <tr>
                  <td> Uptime </td>
                  <td> $(uptime | sed 's/^.*up *//;s/, *[0-9]* user.*$/m/; s/ day[^0-9]*/d, /;s/ \([hms]\).*m$/\1/;s/:/h, /') </td>
                </tr>
                <tr>
                  <td> Load Average </td>
                  <td> $(uptime | awk -F': ' '{print $2}') </td>
                </tr>
              </tbody>
            </table>
        </div>
    </div>
</div>

<!-- Network -->
<div class='card status_card'>
    <header class='card-header'><p class='card-header-title'>Network (WLAN0)</p></header>
    <div class='card-content'>
        <div class='content'>
            <table>
              <tbody>
                <tr>
                  <td> SSID </td>
                  <td> $(/system/bin/iwgetid -r) </td>
                </tr>
                <tr>
                  <td> Link Quality </td>
                  <td> $(cat /proc/net/wireless | awk 'END { print $3 }' | sed 's/\.$//') </td>
                </tr>
                <tr>
                  <td> IP Address </td>
                  <td> $(ifconfig | grep -E "([0-9]{1,3}\.){3}[0-9]{1,3}" | grep -v 127.0.0.1 | awk '{ print $2 }' | cut -f2 -d:) </td>
                </tr>
                <tr>
                  <td> MAC Address </td>
                  <td> $(cat /sys/class/net/wlan0/address) </td>
                </tr>
                <tr>
                  <td> Netmask </td>
                  <td> $(ifconfig wlan0 | sed -rn '2s/ .*:(.*)$/\1/p') </td>
                </tr>
                <tr>
                  <td> Gateway </td>
                  <td> $(route | awk '/default/ { print $2}') </td>
                </tr>
                <tr>
                  <td> DNS </td>
                  <td> <pre>$(cat /etc/resolv.conf) </pre></td>
                </tr>
              </tbody>
            </table>
        </div>
    </div>
</div>

<!-- Bootloader -->
<div class='card status_card'>
    <header class='card-header'><p class='card-header-title'>Bootloader</p></header>
    <div class='card-content'>
        Bootloader MD5:
        <pre>$(md5sum /dev/mtd0 |cut -f 1 -d " ")</pre>
        Bootloader Version:
        <pre>$(busybox strings /dev/mtd0 | grep "U-Boot 2")</pre>
        Your CMDline is:
        <pre>$(cat /proc/cmdline)</pre>


        <a target="_blank" href="cgi-bin/dumpbootloader.cgi">Download Bootloader</a>
    </div>
</div>



EOF
