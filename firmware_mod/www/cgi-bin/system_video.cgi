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

<!-- Video settings -->
<div class='card status_card'>
    <header class='card-header'><p class='card-header-title'>Video Settings</p></header>
    <div class='card-content'>
        <form id="formResolution" action="cgi-bin/action.cgi?cmd=set_video_size" method="post">

            <div class="columns">
                <div class="column">
                    <div class="field is-horizontal">
                        <div class="field-body">
                            <div class="field-label is-normal">
                                <label class="label">Video username</label>
                            </div>
                            <div class="field">
                                <div class="control">
                                    <input class="input" id="videouser" name="videouser" type="text" size="12" value="$(source /system/sdcard/config/rtspserver.conf; echo $USERNAME)" />
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="column">
                    <div class="field-body">
                        <div class="field-label is-normal">
                            <label class="label">Video password</label>
                        </div>
                        <div class="field">
                            <div class="control">
                                <input class="input" id="videopassword" name="videopassword" type="password" size="12" value="$(source /system/sdcard/config/rtspserver.conf; echo $USERPASSWORD)" />
                            </div>
                        </div>
                    </div>
                </div>
                  <div class="column">
                <div class="field-body">
                    <div class="field-label is-normal">
                        <label class="label">Video port</label>
                    </div>
                    <div class="field">
                        <div class="control">
                            <input class="input" id="videoport" name="videoport" type="number" size="12" value=$(source /system/sdcard/config/rtspserver.conf; echo $PORT) />
                        </div>
                    </div>
                    <span class="help">
                        Default is 8554
                    </span>
                </div>
            </div>
           </div>
        <div class="columns">
        <div class="column">


            <div class="field is-horizontal">
                <div class="field-label is-normal">
                    <label class="label">Video Size</label>
                </div>
                <div class="field-body">
                    <div class="field">
                        <div class="control">
                            <div class="select">
                                <select name="video_size">
                                <option value="-W640 -H360"   $(source /system/sdcard/config/rtspserver.conf; if [ "$RTSPH264OPTS" == "-W640 -H360" ]; then echo selected; fi) >640x360</option>
                                <option value="-W768 -H432"   $(source /system/sdcard/config/rtspserver.conf; if [ "$RTSPH264OPTS" == "-W768 -H432" ]; then echo selected; fi) >768x432</option>
                                <option value="-W960 -H540"   $(source /system/sdcard/config/rtspserver.conf; if [ "$RTSPH264OPTS" == "-W960 -H540" ]; then echo selected; fi) >960x540</option>
                                <option value="-W1280 -H720"  $(source /system/sdcard/config/rtspserver.conf; if [ "$RTSPH264OPTS" == "-W1280 -H720" ] || [ -z "$RTSPH264OPTS" ]; then echo selected; fi) >1280x720</option>
                                <option value="-W1600 -H900"  $(source /system/sdcard/config/rtspserver.conf; if [ "$RTSPH264OPTS" == "-W1600 -H900" ]; then echo selected; fi) >1600x900</option>
                                <option value="-W1920 -H1080" $(source /system/sdcard/config/rtspserver.conf; if [ "$RTSPH264OPTS" == "-W1920 -H1080" ]; then echo selected; fi) >1920x1080</option>
                                </select>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="field is-horizontal">
                <div class="field-label is-normal">
                    <label class="label">Video format</label>
                 </div>
                 <div class="field-body">
                    <div class="field">
                        <div class="control">
                            <div class="select">
                                <select name="video_format">
                                0 = FixedQp, 1 = CBR, 2 = VBR, 3 = SMART
                                <option value="0" $(source /system/sdcard/config/rtspserver.conf; if [ "$(echo $VIDEOFORMAT | grep -w 0)" != "" ]; then echo selected; fi)>FixedQp</option>
                                <option value="1" $(source /system/sdcard/config/rtspserver.conf; if [ "$(echo $VIDEOFORMAT | grep -w 1)" != "" ]; then echo selected; fi)>CBR</option>
                                <option value="2" $(source /system/sdcard/config/rtspserver.conf; if [ "$(echo $VIDEOFORMAT | grep -w 2)" != "" ] || [ -z "$VIDEOFORMAT" ] ; then echo selected; fi)>VBR</option>
                                <option value="3" $(source /system/sdcard/config/rtspserver.conf; if [ "$(echo $VIDEOFORMAT | grep -w 3)" != "" ]; then echo selected; fi)>SMART</option>
                                </select>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="field is-horizontal">

                <div class="field-body">
                    <div class="field-label is-horizontal">
                        <label class="label">FrameRate: number of image(s) </label>
                    </div>

                    <div class="field">
                        <div class="control">
                            <input class="input" id="frmRateNum" name="frmRateNum" type="text" size="5" value="$(source /system/sdcard/config/rtspserver.conf; echo $FRAMERATE_NUM)" placeholder="25"/>
                        </div>
                    </div>
                    <div class="field-label is-horizontal">
                        <label class="label">per </label>
                    </div>
                      <div class="field">
                        <div class="control">
                            <input class="input" id="frmRateDen" name="frmRateDen" type="text" size=5 value="$(source /system/sdcard/config/rtspserver.conf; echo $FRAMERATE_DEN)"  placeholder="1" />
                        </div>
                    </div>

                    <div class="field-label is-horizontal">
                      <label class="label"> second(s) </label>
                    </div>
                </div>
            </div>
        </div>
        <div class="column">
            <div class="field is-horizontal">
                <div class="field-label is-normal">
                    <label class="label">bitrate</label>
                </div>
                <div class="field-body">
                    <div class="field">
                        <div class="control">
                            <input class="input" id="brbitrate" name="brbitrate" type="text" size="5" value="$(/system/sdcard/bin/setconf -g b)"/> kbps
                        </div>
                    </div>
                </div>
            </div>
        </div>
        </div>
        <div class="field is-horizontal">
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

<!-- Video Test -->
<div class='card status_card'>
    <header class='card-header'><p class='card-header-title'>Video Test</p></header>
    <div class='card-content'>
        <div class="columns">
            <div class="column">
                <div class="buttons">
                    <a class="button is-link" href='cgi-bin/currentpic.cgi' target='_blank'>Get Image</a>
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
            <button class="button is-link" onClick="call('cgi-bin/action.cgi?cmd=auto_night_mode_start')">On</button>
            <button class="button is-warning" onClick="call('cgi-bin/action.cgi?cmd=auto_night_mode_stop')">Off</button>
            <input class="is-checkradio" id="night_config_hw" type="radio" name="night_config" $(if [ "$(grep -q -e "=hw" /system/sdcard/config/autonight.conf; echo $?)" != 0 ]; then echo "checked";  fi) onClick="call('cgi-bin/action.cgi?cmd=autonight_hw')" >
            <label for="night_config_hw">HW</label>
            <input class="is-checkradio" id="night_config_sw" type="radio" name="night_config" $(if [ "$(grep -q -e "=sw" /system/sdcard/config/autonight.conf; echo $?)" == 0 ]; then echo "checked";  fi)  onClick="call('cgi-bin/action.cgi?cmd=autonight_sw')">
            <label for="night_config_sw">SW</label>
        </div>
        <div class="column">
        <form id="formldr" action="cgi-bin/action.cgi?cmd=setldravg" method="post">
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
            <button class="button is-link" onClick="call('cgi-bin/action.cgi?cmd=toggle-rtsp-nightvision-on')">On</button>
            <button class="button is-warning" onClick="call('cgi-bin/action.cgi?cmd=toggle-rtsp-nightvision-off')">Off</button>
            </div>
        </div>

        <div class="column">
        <br>
        <div class="field is-horizontal">
          <div class="field">
            <input class="switch" name="flip" id="flip" type="checkbox" $(if [ "$(/system/sdcard/bin/setconf -g f)" == 1 ]; then echo "checked";  fi) >
            <label for="flip">Image flip</label>
          </div>

         </div>


        </div>

        </div>
    </div>
</div>

<!-- H264 RTSP -->
<div class='card status_card'>
    <header class='card-header'><p class='card-header-title'>Start H264 RTSP</p></header>
    <div class='card-content'>
        <button class="button is-link" onClick="call('cgi-bin/action.cgi?cmd=h264_start')">Start</button>
        <button class="button is-warning" onClick="call('cgi-bin/action.cgi?cmd=rtsp_stop')">Stop</button>
EOF

PATH="/bin:/sbin:/usr/bin:/media/mmcblk0p2/data/bin:/media/mmcblk0p2/data/sbin:/media/mmcblk0p2/data/usr/bin"

IP=$(ifconfig wlan0 |grep "inet addr" |awk '{print $2}' |awk -F: '{print $2}')
echo "<p>Path to feed: <a href='rtsp://$IP:$(source /system/sdcard/config/rtspserver.conf; echo $PORT)/unicast'>rtsp://$IP:$(source /system/sdcard/config/rtspserver.conf; echo $PORT)/unicast</a></p>"
echo "<p>HLS: <a href='http://$IP:$(source /system/sdcard/config/rtspserver.conf; echo $PORT)/unicast.m3u8'>http://$IP:$(source /system/sdcard/config/rtspserver.conf; echo $PORT)/unicast.m3u8</a></p>"
echo "<p>hls.js web player: <a href='http://$IP:$(source /system/sdcard/config/rtspserver.conf; echo $PORT)'>http://$IP:$(source /system/sdcard/config/rtspserver.conf; echo $PORT)</a></p>"
echo "<p>MPEG-DASH: <a href='http://$IP:$(source /system/sdcard/config/rtspserver.conf; echo $PORT)/unicast.mpd'>http://$IP:$(source /system/sdcard/config/rtspserver.conf; echo $PORT)/unicast.mpd</a></p>"
echo "HLS & MPEG-DASH require the rtspserver to be started with the -S flag. This may reduce the compatibility with some ip camera viewers such as ipcamviewer etc."
cat << EOF
    </div>
</div>

<!-- MJPEG RTSP -->
<div class='card status_card'>
    <header class='card-header'><p class='card-header-title'>Start MJPEG RTSP</p></header>
    <div class='card-content'>
        <button class="button is-link" onClick="call('cgi-bin/action.cgi?cmd=mjpeg_start')">Start</button>
        <button class="button is-warning" onClick="call('cgi-bin/action.cgi?cmd=rtsp_stop')">Stop</button>
EOF

PATH="/bin:/sbin:/usr/bin:/media/mmcblk0p2/data/bin:/media/mmcblk0p2/data/sbin:/media/mmcblk0p2/data/usr/bin"

IP=$(ifconfig wlan0 |grep "inet addr" |awk '{print $2}' |awk -F: '{print $2}')
echo "<p>Path to feed : <a href='rtsp://$IP:$(source /system/sdcard/config/rtspserver.conf; echo $PORT)/unicast'>rtsp://$IP:$(source /system/sdcard/config/rtspserver.conf; echo $PORT)/unicast</a></p>"

cat << EOF
    </div>
</div>

<!-- Timelapse Config-->
<div class='card status_card'>
    <header class='card-header'><p class='card-header-title'>Timelapse Settings</p></header>
    <div class='card-content'>
        <form id="formTimelapse" action="cgi-bin/action.cgi?cmd=conf_timelapse" method="post">
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
                    <p class="help">These settings configure the timelapse mode. Start the timelapse on the Services page.</p>
                </div>
            </div>
        </div>
        <div class="field is-horizontal">
            <div class="field-label is-normal">
            </div>
            <div class="field-body">
                <div class="field">
                <div class="control">
                    <input id="tlSubmit" class="button is-primary" type="submit" value="Save Configuration" />
                </div>
                </div>
            </div>
        </div>
        </form>
    </div>
</div>

EOF
script=$(cat /system/sdcard/www/scripts/status.cgi.js)
echo "<script>$script</script>"
