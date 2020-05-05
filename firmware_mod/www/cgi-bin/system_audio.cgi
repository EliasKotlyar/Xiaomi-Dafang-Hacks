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
<!-- Audio Settings -->
<div class='card status_card'>
    <header class='card-header'>
        <p class='card-header-title'>Audio Settings</p>
    </header>
    <div class='card-content'>
        <form id="formaudioin" action="cgi-bin/action.cgi?cmd=conf_audioin" method="post">

                    <div class="field is-horizontal">
                        <div class="field-label is-normal">
                            <label class="label">Select audio format</label>
                        </div>

                        <div class="field-body">
                            <div class="select">
                                <select name="audioinFormat">
                                       <option value="OFF" $(source /system/sdcard/config/rtspserver.conf; if [ "$(echo $AUDIOFORMAT | grep OFF)" != "" ]; then echo selected; fi)>OFF</option>
                                       <option value="OPUS" $(source /system/sdcard/config/rtspserver.conf; if [ "$(echo $AUDIOFORMAT | grep OPUS)" != "" ]; then echo selected; fi)>OPUS</option>
                                       <option value="PCM"  $(source /system/sdcard/config/rtspserver.conf; if [ "$(echo $AUDIOFORMAT | grep -w PCM)" != "" ]; then echo selected; fi)>PCM</option>
                                       <option value="PCMU" $(source /system/sdcard/config/rtspserver.conf; if [ "$(echo $AUDIOFORMAT | grep -w PCMU)" != "" ]; then echo selected; fi)>PCMU</option>
                                       <option value="MP3" $(source /system/sdcard/config/rtspserver.conf; if [ "$(echo $AUDIOFORMAT | grep -w MP3)" != "" ]; then echo selected; fi)>MP3</option>
                                </select>
                            </div>
                            <span class="help">
                                Needs a restart to become active.
                            </span>
                        </div>
                    </div>
                    <div class="columns">
                    <div class="column">
                    <div class="field is-horizontal">
                        <div class="field-label is-normal">
                            <label class="label">Select in sample rate</label>
                        </div>
                        <div class="field-body">
                                <div class="select">
                                    <select name="audioinBR">
                                           <option value="8000"  $(source /system/sdcard/config/rtspserver.conf; if [ "$(echo $AUDIOINBR | grep 8000)" != "" ]; then echo selected; fi)>8000</option>
                                           <option value="16000" $(source /system/sdcard/config/rtspserver.conf; if [ "$(echo $AUDIOINBR | grep 16000)" != "" ]; then echo selected; fi)>16000</option>
                                           <option value="24000" $(source /system/sdcard/config/rtspserver.conf; if [ "$(echo $AUDIOINBR | grep -w 24000)" != "" ]; then echo selected; fi)>24000</option>
                                           <option value="44100" $(source /system/sdcard/config/rtspserver.conf; if [ "$(echo $AUDIOINBR | grep -w 44100)" != "" ]; then echo selected; fi)>44100</option>
                                           <option value="48000" $(source /system/sdcard/config/rtspserver.conf; if [ "$(echo $AUDIOINBR | grep -w 48000)" != "" ]; then echo selected; fi)>48000</option>
                                    </select>
                                </div>
                                <span class="help">
                                   Above 16000 some filters become inactive
                                </span>
                        </div>
                    </div>

                    <div class="field is-horizontal">
                        <div class="field-label is-normal">
                            <label class="label">Filter (low filter)</label>
                        </div>
                        <div class="field-body">
                            <div class="select">
                                <select name="audioinFilter">
                                       <option value="0" $(if [ "$(/system/sdcard/bin/setconf -g q)" == "0" ]; then echo selected; fi)>No filter</option>
                                       <option value="1" $(if [ "$(/system/sdcard/bin/setconf -g q)" == "1" ]; then echo selected; fi)>Filter 1</option>
                                       <option value="2" $(if [ "$(/system/sdcard/bin/setconf -g q)" == "2" ]; then echo selected; fi)>Filter 2</option>
                                       <option value="3" $(if [ "$(/system/sdcard/bin/setconf -g q)" == "3" ]; then echo selected; fi)>NS Filter LOW</option>
                                       <option value="4" $(if [ "$(/system/sdcard/bin/setconf -g q)" == "4" ]; then echo selected; fi)>NS Filter MODERATE</option>
                                       <option value="5" $(if [ "$(/system/sdcard/bin/setconf -g q)" == "5" ]; then echo selected; fi)>NS Filter HIGH</option>
                                       <option value="6" $(if [ "$(/system/sdcard/bin/setconf -g q)" == "6" ]; then echo selected; fi)>NS Filter VERY HIGH</option>
                                </select>
                            </div>
                        </div>
                    </div>
                    <div class="field is-horizontal">
                        <div class="field-label is-normal">
                            <label class="label">High pass filter</label>
                        </div>
                        <div class="field-body">
                            <p class="control">
                                <div class="double">
                                    <input type="checkbox" name="HFEnabled" value="enabled" $(if [ "$(/system/sdcard/bin/setconf -g l)" == "true" ]; then echo checked; fi)/>
                                </div>
                            </p>
                        </div>
                    </div>
                </div>
                <div class="column">
                     <div class="field is-horizontal">
                            <div class="field-label is-normal">
                                <label class="label">Select out sample rate</label>
                            </div>
                            <div class="field-body">
                                <div class="select">
                                    <select name="audiooutBR">
                                           <option value="8000"  $(source /system/sdcard/config/rtspserver.conf; if [ "$(echo $AUDIOOUTBR | grep 8000)" != "" ]; then echo selected; fi)>8000</option>
                                           <option value="16000" $(source /system/sdcard/config/rtspserver.conf; if [ "$(echo $AUDIOOUTBR | grep 16000)" != "" ]; then echo selected; fi)>16000</option>
                                           <option value="24000" $(source /system/sdcard/config/rtspserver.conf; if [ "$(echo $AUDIOOUTBR | grep -w 24000)" != "" ]; then echo selected; fi)>24000</option>
                                           <option value="44100" $(source /system/sdcard/config/rtspserver.conf; if [ "$(echo $AUDIOOUTBR | grep -w 44100)" != "" ]; then echo selected; fi)>44100</option>
                                           <option value="48000" $(source /system/sdcard/config/rtspserver.conf; if [ "$(echo $AUDIOOUTBR | grep -w 48000)" != "" ]; then echo selected; fi)>48000</option>
                                    </select>
                                </div>

                            </div>
                        </div>

                    <div class="field is-horizontal">
                        <div class="field-label is-normal">
                            <label class="label">Volume</label>
                        </div>
                        <input class="slider is-fullwidth" name="audioinVol" step="1" min="-1" max="120" value="$(/system/sdcard/bin/setconf -g h)" type="range">
                    </div>
                    <br><br>
                    <div class="field is-horizontal">
                        <div class="field-label is-normal">
                            <label class="label">AEC filter</label>
                        </div>
                        <div class="field-body">
                            <p class="control">
                                <div class="double">
                                    <input type="checkbox" name="AECEnabled" value="enabled" $(if [ "$(/system/sdcard/bin/setconf -g a)" == "true" ]; then echo checked; fi)/>
                                </div>
                            </p>
                        </div>
                    </div>

                </div>
            </div>
            <p class="control">
                <input id="audioinSubmit" class="button is-primary" type="submit" value="Set" />
            </p>
        </form>
    </div>
</div>

<!-- Audio Testing -->
<div class='card status_card'>
    <header class='card-header'><p class='card-header-title'>Audio Test</p></header>
    <div class='card-content'>
        <div class="columns">
        <div class="column">
            <form id="formAudio" action="cgi-bin/action.cgi?cmd=audio_test" method="post">
                <label>Audio Output Test</label>
                <div class="select">
                    <select name="audioSource">
                        $(
                           for i in `/system/sdcard/bin/busybox find /usr/share/notify/ /system/sdcard/media -name *.wav`
                           do
                                echo  "<option value=$i> `/system/sdcard/bin/busybox basename $i` </option>"
                           done
                        )
                    </select>
                </div>
                <input class="slider is-fullwidth" name="audiotestVol" step="1" min="0" max="120" value="50" type="range">

                <div class="field-body">
                    <div class="field">
                        <div class="control">
                            <input id="AudioTestSubmit" class="button is-primary" type="submit" value="Play" />
                        </div>
                    </div>
                </div>
            </form>
        </div>
        </div>
    </div>
</div>

EOF
script=$(cat /system/sdcard/www/scripts/status.cgi.js)
echo "<script>$script</script>"
