#!/bin/sh

echo "Content-type: text/html"
echo "Pragma: no-cache"
echo "Cache-Control: max-age=0, no-store, no-cache"
echo ""

# source header.cgi

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
<script>
    function call(url){
            var xhr = new XMLHttpRequest();
            xhr.open('GET', url, true);
            xhr.send();
    }

</script>

<!-- Motor -->
<div class='card status_card'>
    <header class='card-header'><p class='card-header-title'>Motor</p></header>
    <div class='card-content'>
        <table class="motor_control">
            <tr>
                <td></td>
                <td>
                    <button class="button is-link" onclick="call('cgi-bin/action.cgi?cmd=motor_up&val='+document.getElementById('val').value)">&uarr; Up</button>
                </td>
                <td></td>
            </tr>
            <tr>
                <td>
                    <button class="button is-link" onclick="call('cgi-bin/action.cgi?cmd=motor_left&val='+document.getElementById('val').value)">&larr; Left</button>
                </td>
                <td>
                    <input class="input has-text-centered" type="text" id="val" name="val" value="100">
                </td>
                <td>
                    <button class="button is-link" onclick="call('cgi-bin/action.cgi?cmd=motor_right&val='+document.getElementById('val').value)">Right &rarr;</button>
                </td>
            </tr>
            <tr>
                <td></td>
                <td>
                    <button class="button is-link" onclick="call('cgi-bin/action.cgi?cmd=motor_down&val='+document.getElementById('val').value)">&darr; Down</button>
                </td>
                <td></td>
            </tr>
        </table>
        <div class="buttons">
        <button class="button is-warning" onclick="call('cgi-bin/action.cgi?cmd=motor_calibrate')">Calibrate</button>
        </div>
    </div>
</div>

EOF
script=$(cat /system/sdcard/www/scripts/status.cgi.js)
echo "<script>$script</script>"
