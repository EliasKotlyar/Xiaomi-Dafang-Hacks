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

<!-- OSD -->
<div class='card status_card'>
    <header class='card-header'><p class='card-header-title'>OSD Display</p></header>
    <div class='card-content'>
        <form id="formOSD" action="cgi-bin/action.cgi?cmd=osd" method="post">

            <div class="field is-horizontal">
                <div class="field-label is-normal">
                    <label class="label">Enable Text</label>
                </div>
                <div class="field-body">
                    <div class="field is-grouped">
                        <p class="control">
                            <input type="checkbox" name="OSDenable" value="enabled" $(if [ "$(grep ENABLE_OSD /system/sdcard/config/osd.conf | sed s/ENABLE_OSD=//)" == "true" ]; then echo checked; fi) />
                        </p>
                        <p class="control">
                            <input class="input" id="osdtext" name="osdtext" type="text" size="25" value="$(source /system/sdcard/config/osd.conf && echo "$OSD")"/>
                            <span class="help">
                                Enter time-variables in <a href="http://strftime.org/" target="_blank">strftime</a> format
                            </span>
                        </p>
                    </div>
                </div>
            </div>
            <div class="field is-horizontal">
                <div class="field-label is-normal">
                    <label class="label">Enable Axis</label>
                </div>
                <div class="field-body">
                    <div class="field is-grouped">
                        <p class="control">
                            <input type="checkbox" name="AXISenable" value="enabled" $(if [[ "$(grep DISPLAY_AXIS /system/sdcard/config/osd.conf | sed s/DISPLAY_AXIS=//)" == "true" ]];then echo checked; fi) />
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
                                <option value="0" $(if [ "$(grep COLOR /system/sdcard/config/osd.conf | sed s/COLOR=//)" -eq 0 ]; then echo selected; fi)>White</option>
                                <option value="1" $(if [ "$(grep COLOR /system/sdcard/config/osd.conf | sed s/COLOR=//)" -eq 1 ]; then echo selected; fi)>Black</option>
                                <option value="2" $(if [ "$(grep COLOR /system/sdcard/config/osd.conf | sed s/COLOR=//)" -eq 2 ]; then echo selected; fi)>Red</option>
                                <option value="3" $(if [ "$(grep COLOR /system/sdcard/config/osd.conf | sed s/COLOR=//)" -eq 3 ]; then echo selected; fi)>Green</option>
                                <option value="4" $(if [ "$(grep COLOR /system/sdcard/config/osd.conf | sed s/COLOR=//)" -eq 4 ]; then echo selected; fi)>Blue</option>
                                <option value="5" $(if [ "$(grep COLOR /system/sdcard/config/osd.conf | sed s/COLOR=//)" -eq 5 ]; then echo selected; fi)>Cyan</option>
                                <option value="6" $(if [ "$(grep COLOR /system/sdcard/config/osd.conf | sed s/COLOR=//)" -eq 6 ]; then echo selected; fi)>Yellow</option>
                                <option value="7" $(if [ "$(grep COLOR /system/sdcard/config/osd.conf | sed s/COLOR=//)" -eq 7 ]; then echo selected; fi)>Purple</option>
                                </select>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="field is-horizontal">
                <div class="field-label is-normal">
                    <label class="label">Font name</label>
                </div>
                <div class="field-body">
                    <div class="field">
                        <div class="control">
                            <div class="select">
                                <select name="FontName">
                                    $(
                                       fontName="$(/system/sdcard/bin/setconf -g e)"
                                       echo -n "<option value=\"\""
                                       if [ -n "${fontName-unset}" ] ; then echo selected; fi
                                       echo -n ">Default fonts </option>"

                                       for i in `/system/sdcard/bin/busybox find /system/sdcard/fonts -name *.ttf`
                                       do
                                            echo -n "<option value=\"$i\" "
                                            if [ "$fontName" == "$i" ] ; then echo selected; fi
                                            echo -n ">`/system/sdcard/bin/busybox basename $i` </option>"
                                       done
                                    )
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
                        <p class="control">
                                 <input class="input" id="OSDSize" name="OSDSize" type="number" size="4"
                                     value="$(
                                        fontSize=$(/system/sdcard/bin/setconf -g s)
                                        if [ "$fontSize" == "0" ]; then echo 18
                                        elif [ "$fontSize" == "1" ]; then echo 40
                                        else echo "$fontSize"
                                        fi
                                     )"/>
                        </p>
                         <p class="help">Too high value won't display anything</p>
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
                            <input class="input" id="spacepixels" name="spacepixels" type="number" size="4" value="$(source /system/sdcard/config/osd.conf && echo "$SPACE")"/>
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
                            <input class="input" id="posy" name="posy" type="number" size="6" value="$(source /system/sdcard/config/osd.conf && echo "$POSY")"/>
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
                                <option value="0" $(if [ "$(grep FIXEDW /system/sdcard/config/osd.conf | sed s/FIXEDW=//)" -eq 0 ]; then echo selected; fi)>No</option>
                                <option value="1" $(if [ "$(grep FIXEDW /system/sdcard/config/osd.conf | sed s/FIXEDW=//)" -eq 1 ]; then echo selected; fi)>Yes</option>
                                </select>
                            </div>
                            <p class="help">Fixed width works only for "default" fonts</p>
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
        <button class="button is-link" onClick="call('cgi-bin/action.cgi?cmd=onDebug')">On</button>
        <button class="button is-warning" onClick="call('cgi-bin/action.cgi?cmd=offDebug')">Off</button>
    </div>
</div>

EOF
script=$(cat /system/sdcard/www/scripts/status.cgi.js)
echo "<script>$script</script>"
