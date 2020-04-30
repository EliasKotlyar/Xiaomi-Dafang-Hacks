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

<!-- Blue / Yellow LED -->
<div class='card status_card'>
    <header class='card-header'><p class='card-header-title'>LED</p></header>
    <div class='card-content'>
        <div class="columns">
        <div class="column">
            <label>Blue LED</label>
            <div class="buttons">
                <button class="button is-link" onClick="call('cgi-bin/action.cgi?cmd=blue_led_on')">On</button>
                <button class="button is-warning" onClick="call('cgi-bin/action.cgi?cmd=blue_led_off')">Off</button>
            </div>
        </div>

        <div class="column">
            <label>Yellow LED</label>
            <div class="buttons">
                <button class="button is-link" onClick="call('cgi-bin/action.cgi?cmd=yellow_led_on')">On</button>
                <button class="button is-warning" onClick="call('cgi-bin/action.cgi?cmd=yellow_led_off')">Off</button>
            </div>
        </div>

        </div>
    </div>
</div>

<!-- IR LED / (Filter)Cut-->
<div class='card status_card'>
    <header class='card-header'><p class='card-header-title'>IR</p></header>
    <div class='card-content'>
        <div class="columns">
        <div class="column">
            <label>IR LED</label>
            <div class="buttons">
            <button class="button is-link" onClick="call('cgi-bin/action.cgi?cmd=ir_led_on')">On</button>
            <button class="button is-warning" onClick="call('cgi-bin/action.cgi?cmd=ir_led_off')">Off</button>
            </div>
        </div>

        <div class="column">
            <label>IR Filter</label>
            <div class="buttons">
            <button class="button is-link" onClick="call('cgi-bin/action.cgi?cmd=ir_cut_on')">On</button>
            <button class="button is-warning" onClick="call('cgi-bin/action.cgi?cmd=ir_cut_off')">Off</button>
            </div>
        </div>
        </div>
    </div>
</div>

EOF
script=$(cat /system/sdcard/www/scripts/status.cgi.js)
echo "<script>$script</script>"
