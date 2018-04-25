#!/bin/sh

echo "Content-type: text/html"
echo "Pragma: no-cache"
echo "Cache-Control: max-age=0, no-store, no-cache"
echo ""

# source header.cgi

cat << EOF
<!-- Date -->
<div class='card status_card'>
    <header class='card-header'><p class='card-header-title'>System</p></header>
    <div class='card-content'>
    <form id="tzForm" action="/cgi-bin/action.cgi?cmd=settz" method="post">

        <div class="field is-horizontal">
            <div class="field-label is-normal">
                <label class="label" for="tz">TZ</label>
            </div>
            <div class="field-body">
                <div class="field">
                    <div class="control">
                        <input class="input" id="tz" name="tz" type="text" size="25" value="$(cat /etc/TZ)" />
                    </div>
                    <p>$(date)</p>
                </div>
            </div>
        </div>
        <div class="field is-horizontal">
            <div class="field-label is-normal">
                <label class="label" for="ntp_srv">NTP Server</label>
            </div>
            <div class="field-body">
                <div class="field">
                    <div class="control">
                        <input class="input" id="ntp_srv" name="ntp_srv" type="text" size="25" value="$(cat /system/sdcard/config/ntp_srv.conf)" />
                    </div>
                </div>
            </div>
        </div>
        <div class="field is-horizontal">
            <div class="field-label is-normal">
                <label class="label" for="hostname">Hostname</label>
            </div>
            <div class="field-body">
                <div class="field">
                <div class="control">
                    <input class="input" id="hostname" name="hostname" type="text" size="15" value="$(hostname)" />
                </div>
                </div>
            </div>
        </div>
        <div class="field is-horizontal">
            <div class="field-label is-normal">
            </div>
            <div class="field-body">
                <div class="field">
                <div class="control">
                    <input id="tzSubmit" class="button is-primary" type="submit" value="Set" />
                </div>
                </div>
            </div>
        </div>
    </form>
    </div>
</div>
<!-- Version -->
<div class='card status_card'>
    <header class='card-header'><p class='card-header-title'>Version</p></header>
    <div class='card-content'>
    <p>$(cut -d'=' -f2 /etc/os-release)</p>
    </div>
</div>

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
                <button class="button is-link" onClick="call('/cgi-bin/action.cgi?cmd=blue_led_on')">On</button>
                <button class="button is-warning" onClick="call('/cgi-bin/action.cgi?cmd=blue_led_off')">Off</button>
            </div>
        </div>

        <div class="column">
            <label>Yellow LED</label>
            <div class="buttons">
                <button class="button is-link" onClick="call('/cgi-bin/action.cgi?cmd=yellow_led_on')">On</button>
                <button class="button is-warning" onClick="call('/cgi-bin/action.cgi?cmd=yellow_led_off')">Off</button>
            </div>
        </div>

        </div>
    </div>
</div>

<!-- IR LED / Cut-->
<div class='card status_card'>
    <header class='card-header'><p class='card-header-title'>IR</p></header>
    <div class='card-content'>
        <div class="columns">
        <div class="column">
            <label>IR LED</label>
            <div class="buttons">
            <button class="button is-link" onClick="call('/cgi-bin/action.cgi?cmd=ir_led_on')">On</button>
            <button class="button is-warning" onClick="call('/cgi-bin/action.cgi?cmd=ir_led_off')">Off</button>
            </div>
        </div>

        <div class="column">
            <label>IR Cut</label>
            <div class="buttons">
            <button class="button is-link" onClick="call('/cgi-bin/action.cgi?cmd=ir_cut_on')">On</button>
            <button class="button is-warning" onClick="call('/cgi-bin/action.cgi?cmd=ir_cut_off')">Off</button>
            </div>
        </div>
        </div>
    </div>
</div>

<!-- Auto Night Mode -->
<div class='card status_card'>
    <header class='card-header'><p class='card-header-title'>Auto Night Mode</p></header>
    <div class='card-content'>
        <div class="columns">
        <div class="column">
            <button class="button is-link" onClick="call('/cgi-bin/action.cgi?cmd=auto_night_mode_start')">On</button>
            <button class="button is-warning" onClick="call('/cgi-bin/action.cgi?cmd=auto_night_mode_stop')">Off</button>
        </div>
        <div class="column">
        <form id="formldr" action="/cgi-bin/action.cgi?cmd=setldravg" method="post">
            <p>Use average measurement on switching.</p>
            <label class="label">Number of measurements</label>
            <div class="field is-grouped">
                <div class="control">
                    <div class="select">
                        <select class="select" name="avg">
                            <option value="1" $(if [ "$(sed s/AVG=// /system/sdcard/config/ldr-average.conf)" -eq 1 ]; then echo selected; fi)>1</option>
                            <option value="2" $(if [ "$(sed s/AVG=// /system/sdcard/config/ldr-average.conf)" -eq 2 ]; then echo selected; fi)>2</option>
                            <option value="3" $(if [ "$(sed s/AVG=// /system/sdcard/config/ldr-average.conf)" -eq 3 ]; then echo selected; fi)>3</option>
                            <option value="4" $(if [ "$(sed s/AVG=// /system/sdcard/config/ldr-average.conf)" -eq 4 ]; then echo selected; fi)>4</option>
                            <option value="5" $(if [ "$(sed s/AVG=// /system/sdcard/config/ldr-average.conf)" -eq 5 ]; then echo selected; fi)>5</option>
                            <option value="10" $(if [ "$(sed s/AVG=// /system/sdcard/config/ldr-average.conf)" -eq 10 ]; then echo selected; fi)>10</option>
                            <option value="15" $(if [ "$(sed s/AVG=// /system/sdcard/config/ldr-average.conf)" -eq 15 ]; then echo selected; fi)>15</option>
                        </select>
                    </div>
                </div>
                <p class="control">
                    <input id="ldrSubmit" class="button is-primary" type="submit" value="Set" />
                </p>
            </div>
        </form>
        </div>
        </div>
    </div>
</div>

<!-- RTSP -->
<div class='card status_card'>
    <header class='card-header'><p class='card-header-title'>RTSP</p></header>
    <div class='card-content'>
        <div class="columns">

        <div class="column">
            <label>Night Vision</label>
            <div class="buttons">
            <button class="button is-link" onClick="call('/cgi-bin/action.cgi?cmd=toggle-rtsp-nightvision-on')">On</button>
            <button class="button is-warning" onClick="call('/cgi-bin/action.cgi?cmd=toggle-rtsp-nightvision-off')">Off</button>
            </div>
        </div>

        <div class="column">
            <label>Flip</label>
            <div class="buttons">
            <button class="button is-link" onClick="call('/cgi-bin/action.cgi?cmd=flip-on')">On</button>
            <button class="button is-warning" onClick="call('/cgi-bin/action.cgi?cmd=flip-off')">Off</button>
            </div>
        </div>

        </div>
    </div>
</div>

<!-- Motor -->
<div class='card status_card'>
    <header class='card-header'><p class='card-header-title'>Motor</p></header>
    <div class='card-content'>
        <table class="motor_control">
            <tr>
                <td></td>
                <td>
                    <button class="button is-link" onclick="call('/cgi-bin/action.cgi?cmd=motor_up&val='+document.getElementById('val').value)">&uarr; Up</button>
                </td>
                <td></td>
            </tr>
            <tr>
                <td>
                    <button class="button is-link" onclick="call('/cgi-bin/action.cgi?cmd=motor_left&val='+document.getElementById('val').value)">&larr; Left</button>
                </td>
                <td>
                    <input class="input has-text-centered" type="text" id="val" name="val" value="100">
                </td>
                <td>
                    <button class="button is-link" onclick="call('/cgi-bin/action.cgi?cmd=motor_right&val='+document.getElementById('val').value)">Right &rarr;</button>
                </td>
            </tr>
            <tr>
                <td></td>
                <td>
                    <button class="button is-link" onclick="call('/cgi-bin/action.cgi?cmd=motor_down&val='+document.getElementById('val').value)">&darr; Down</button>
                </td>
                <td></td>
            </tr>
        </table>
        <div class="buttons">
        <button class="button is-warning" onclick="call('/cgi-bin/action.cgi?cmd=motor_vcalibrate')">Calibrate Vertical</button>
        <button class="button is-warning" onclick="call('/cgi-bin/action.cgi?cmd=motor_hcalibrate')">Calibrate Horizontal</button>
        </div>
    </div>
</div>

<!-- Audio / Image -->
<div class='card status_card'>
    <header class='card-header'><p class='card-header-title'>Tests</p></header>
    <div class='card-content'>

        <div class="columns">

        <div class="column">
        <label>Audio Test</label>
        <div class="buttons">
        <button class="button is-link" onClick="call('/cgi-bin/action.cgi?cmd=audio_test')">Test</button>
        </div>
        </div>

        <div class="column">
        <label>Image</label>
        <div class="buttons">
        <a class="button is-link" href='/cgi-bin/currentpic.cgi' target='_blank'>Get</a>
        </div>
        </div>

        </div>
    </div>
</div>

<!-- Resolution -->
<div class='card status_card'>
    <header class='card-header'><p class='card-header-title'>Resolution</p></header>
    <div class='card-content'>

        <form id="formResolution" action="/cgi-bin/action.cgi?cmd=set_video_size" method="post">
        <div class="field is-horizontal">
            <div class="field-label is-normal">
                <label class="label">Video Size</label>
            </div>
            <div class="field-body">
                <div class="field">
                    <div class="control">
                        <div class="select">
                            <select name="video_size">
                            <option value="-W640 -H360" $(if [ "$(cat /system/sdcard/config/rtspserver.conf | grep 640)" != "" ]; then echo selected; fi)>640x360</option>
                            <option value="-W960 -H540" $(if [ "$(cat /system/sdcard/config/rtspserver.conf | grep 960)" != "" ]; then echo selected; fi)>960x540</option>
                            <option value="-W1280 -H720" $(if [ "$(cat /system/sdcard/config/rtspserver.conf | grep 1280)" != "" ]; then echo selected; fi)>1280x720</option>
                            <option value="-W1600 -H900" $(if [ "$(cat /system/sdcard/config/rtspserver.conf | grep 1600)" != "" ]; then echo selected; fi)>1600x900</option>
                            <option value="-W1920 -H1080" $(if [ "$(cat /system/sdcard/config/rtspserver.conf | grep 1920)" != "" ]; then echo selected; fi)>1920x1080</option>
                            </select>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="field is-horizontal">
            <div class="field-label is-normal">
            </div>
            <div class="field-body">
                <div class="field">
                <div class="control">
                    <input id="resSubmit" class="button is-primary" type="submit" value="Set" />
                </div>
                </div>
            </div>
        </div>
        </form>
    </div>
</div>

<!-- H264 RTSP -->
<div class='card status_card'>
    <header class='card-header'><p class='card-header-title'>Start H264 RTSP</p></header>
    <div class='card-content'>
        <button class="button is-link" onClick="call('/cgi-bin/action.cgi?cmd=h264_start')">Start</button>
        <button class="button is-warning" onClick="call('/cgi-bin/action.cgi?cmd=rtsp_stop')">Stop</button>
EOF

PATH="/bin:/sbin:/usr/bin:/media/mmcblk0p2/data/bin:/media/mmcblk0p2/data/sbin:/media/mmcblk0p2/data/usr/bin"

IP=$(ifconfig wlan0 |grep "inet addr" |awk '{print $2}' |awk -F: '{print $2}')
echo "<p>Path to feed : <a href='rtsp://$IP:8554/unicast'>rtsp://$IP:8554/unicast</a></p>"
echo "<p>HLS : <a href='http://$IP:8554/unicast.m3u8'>http://$IP:8554/unicast.m3u8</a></p>"
echo "<p>MPEG-DASH : <a href='http://$IP:8554/unicast.mpd'>http://$IP:8554/unicast.mpd</a></p>"

cat << EOF
    </div>
</div>

<!-- MJPEG RTSP -->
<div class='card status_card'>
    <header class='card-header'><p class='card-header-title'>Start MJGEP RTSP</p></header>
    <div class='card-content'>
        <button class="button is-link" onClick="call('/cgi-bin/action.cgi?cmd=mjpeg_start')">Start</button>
        <button class="button is-warning" onClick="call('/cgi-bin/action.cgi?cmd=rtsp_stop')">Stop</button>
EOF

PATH="/bin:/sbin:/usr/bin:/media/mmcblk0p2/data/bin:/media/mmcblk0p2/data/sbin:/media/mmcblk0p2/data/usr/bin"

IP=$(ifconfig wlan0 |grep "inet addr" |awk '{print $2}' |awk -F: '{print $2}')
echo "<p>Path to feed : <a href='rtsp://$IP:8554/unicast'>rtsp://$IP:8554/unicast</a></p>"

cat << EOF
    </div>
</div>

<!-- OSD -->
<div class='card status_card'>
    <header class='card-header'><p class='card-header-title'>OSD Display</p></header>
    <div class='card-content'>
        <form id="formOSD" action="/cgi-bin/action.cgi?cmd=osd" method="post">

            <div class="field is-horizontal">
                <div class="field-label is-normal">
                    <label class="label">Enable Text</label>
                </div>
                <div class="field-body">
                    <div class="field is-grouped">
                        <p class="control">
                            <input type="checkbox" name="OSDenable" value="enabled" $(if [ -f /system/sdcard/config/osd ]; then echo checked; fi) />
                        </p>
                        <p class="control">
                            <input class="input" id="osdtext" name="osdtext" type="text" size="25" value="$(source /system/sdcard/config/osd && echo "$OSD")"/>
                            <span class="help">
                                Enter time-variables in <a href="http://strftime.org/" target="_blank">strftime</a> format
                            </span>
                        </p>
                    </div>
                </div>
            </div>
            <div class="field is-horizontal">
                <div class="field-label is-normal">
                    <label class="label">OSD Color</label>
                </div>
                <div class="field-body">
                    <div class="field">
                        <div class="control">
                            <div class="select">
                                <select name="color">
                                <option value="0" $(if [ "$(grep COLOR /system/sdcard/config/osd | sed s/COLOR=//)" -eq 0 ]; then echo selected; fi)>White</option>
                                <option value="1" $(if [ "$(grep COLOR /system/sdcard/config/osd | sed s/COLOR=//)" -eq 1 ]; then echo selected; fi)>Black</option>
                                <option value="2" $(if [ "$(grep COLOR /system/sdcard/config/osd | sed s/COLOR=//)" -eq 2 ]; then echo selected; fi)>Red</option>
                                <option value="3" $(if [ "$(grep COLOR /system/sdcard/config/osd | sed s/COLOR=//)" -eq 3 ]; then echo selected; fi)>Green</option>
                                <option value="4" $(if [ "$(grep COLOR /system/sdcard/config/osd | sed s/COLOR=//)" -eq 4 ]; then echo selected; fi)>Blue</option>
                                <option value="5" $(if [ "$(grep COLOR /system/sdcard/config/osd | sed s/COLOR=//)" -eq 5 ]; then echo selected; fi)>Cyan</option>
                                <option value="6" $(if [ "$(grep COLOR /system/sdcard/config/osd | sed s/COLOR=//)" -eq 6 ]; then echo selected; fi)>Yellow</option>
                                <option value="7" $(if [ "$(grep COLOR /system/sdcard/config/osd | sed s/COLOR=//)" -eq 7 ]; then echo selected; fi)>Purple</option>
                                </select>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="field is-horizontal">
                <div class="field-label is-normal">
                    <label class="label">OSD Text Size</label>
                </div>
                <div class="field-body">
                    <div class="field">
                        <div class="control">
                            <div class="select">
                                <select name="size">
                                <option value="0" $(if [ "$(grep SIZE /system/sdcard/config/osd | sed s/SIZE=//)" -eq 0 ]; then echo selected; fi)>Small</option>
                                <option value="1" $(if [ "$(grep SIZE /system/sdcard/config/osd | sed s/SIZE=//)" -eq 1 ]; then echo selected; fi)>Bigger</option>
                                </select>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="field is-horizontal">
                <div class="field-label is-normal">
                    <label class="label">Pixels between chars</label>
                </div>
                <div class="field-body">
                    <div class="field">
                        <p class="control">
                            <input class="input" id="spacepixels" name="spacepixels" type="number" size="4" value="$(source /system/sdcard/config/osd && echo "$SPACE")"/>
                        </p>
                        <p class="help">Can be negative</p>
                    </div>
                </div>
            </div>
            <div class="field is-horizontal">
                <div class="field-label is-normal">
                    <label class="label">Y Position</label>
                </div>
                <div class="field-body">
                    <div class="field">
                        <p class="control">
                            <input class="input" id="posy" name="posy" type="number" size="6" value="$(source /system/sdcard/config/osd && echo "$POSY")"/>
                        </p>
                    </div>
                </div>
            </div>

            <div class="field is-horizontal">
                <div class="field-label is-normal">
                    <label class="label">Fixed width</label>
                </div>
                <div class="field-body">
                    <div class="field">
                        <div class="control">
                            <div class="select">
                                <select name="fixedw">
                                <option value="0" $(if [ "$(grep FIXEDW /system/sdcard/config/osd | sed s/FIXEDW=//)" -eq 0 ]; then echo selected; fi)>No</option>
                                <option value="1" $(if [ "$(grep FIXEDW /system/sdcard/config/osd | sed s/FIXEDW=//)" -eq 1 ]; then echo selected; fi)>Yes</option>
                                </select>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="field is-horizontal">
                <div class="field-label is-normal">
                </div>
                <div class="field-body">
                    <div class="field">
                    <div class="control">
                        <input id="osdSubmit" class="button is-primary" type="submit" value="Set" />
                    </div>
                    </div>
                </div>
            </div>
        </form>
    </div>
</div>


<!-- OSD Debug -->
<div class='card status_card'>
    <header class='card-header'><p class='card-header-title'>Display debug info on OSD</p></header>
    <div class='card-content'>
        <button class="button is-link" onClick="call('/cgi-bin/action.cgi?cmd=onDebug')">On</button>
        <button class="button is-warning" onClick="call('/cgi-bin/action.cgi?cmd=offDebug')">Off</button>
    </div>
</div>

<!-- Timelapse -->
<div class='card status_card'>
    <header class='card-header'><p class='card-header-title'>Timelapse</p></header>
    <div class='card-content'>
        <form id="formTimelapse" action="/cgi-bin/action.cgi?cmd=conf_timelapse" method="post">
        <div class="field is-horizontal">
            <div class="field-label is-normal">
                <label class="label">Interval</label>
            </div>
            <div class="field-body">
                <div class="field">
                    <div class="control">
                        <input class="input" id="tlinterval" name="tlinterval" type="text" size="5" value="$(source /system/sdcard/config/timelapse.conf && echo "$TIMELAPSE_INTERVAL")"/> seconds
                    </div>
                </div>
            </div>
        </div>
        <div class="field is-horizontal">
            <div class="field-label is-normal">
                <label class="label">Duration</label>
            </div>
            <div class="field-body">
                <div class="field">
                    <div class="control">
                        <input class="input" id="tlduration" name="tlduration" type="text" size="5" value="$(source /system/sdcard/config/timelapse.conf && echo "$TIMELAPSE_DURATION")"/> minutes
                    </div>
                    <p class="help">Set to 0 for unlimited</p>
                </div>
            </div>
        </div>
        <div class="field is-horizontal">
            <div class="field-label is-normal">
            </div>
            <div class="field-body">
                <div class="field">
                <div class="control">
                    <input id="tlSubmit" class="button is-primary" type="submit" value="Set" />
                </div>
                </div>
            </div>
        </div>
        </form>
    </div>
</div>


<!-- Original Xiaomi Software -->
<div class='card status_card'>
    <header class='card-header'><p class='card-header-title'>Start original Xiaomi Software</p></header>
    <div class='card-content'>
        <button class="button" onClick="call('/cgi-bin/action.cgi?cmd=xiaomi_start')">Start</button>
    </div>
</div>



<!-- Process List -->
<div class='card status_card'>
    <header class='card-header'><p class='card-header-title'>Process List</p></header>
    <div class='card-content'>
        <pre>$(ps)</pre>
    </div>
</div>

<!-- Mounts -->
<div class='card status_card'>
    <header class='card-header'><p class='card-header-title'>Mounts</p></header>
    <div class='card-content'>
        <pre>$(mount)</pre>
    </div>
</div>

EOF
script=$(cat /system/sdcard/www/scripts/status.cgi.js)
echo "<script>$script</script>"
