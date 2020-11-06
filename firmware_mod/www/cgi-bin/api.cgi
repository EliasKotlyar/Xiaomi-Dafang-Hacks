#!/bin/sh

################################################
# Created by Krzysztof Szeremeta (KSZERE)      #
# kszere@gmail.com | 2018-01-31 |  v0.0.5 Beta #
################################################

source ./func.cgi

# START VARIABLES
PATH="/system/bin:/bin:/usr/bin:/sbin:/usr/sbin:/media/mmcblk0p2/data/bin:/media/mmcblk0p2/data/sbin:/media/mmcblk0p2/data/usr/bin"
CONFIGPATH=/system/sdcard/config
BINPATH=/system/sdcard/bin
SDPATH=/system/sdcard
VERSION="v0.0.5 Beta"
MOTOR=/system/sdcard/bin/motor.bin
# END VARIABLES

# START FUNCTIONS
setGpio(){
  GPIOPIN=$1
  echo $2 > /sys/class/gpio/gpio$GPIOPIN/value
}

getReturn(){
echo "Content-type: application/json; charset=utf-8; Pragma: no-cache; Expires: Wednesday, 27-Dec-95 05:29:10 GMT"
echo ""
echo "{
  \"code\": $1,
  \"status\": \"$2\",
  \"description\": \"$3\"
}"
}
#getReturn 123 "sc" "desc"
# END FUNCTIONS

if [ -n "$F_ns" ]; then
  if [ "$F_ns" -le 2500 -a "$F_ns" -ge 0 ]; then
    F_ns=$F_ns
  else
    F_ns=2500
  fi
else
  F_ns=100
fi



export LD_LIBRARY_PATH=/system/lib
export LD_LIBRARY_PATH=/thirdlib:$LD_LIBRARY_PATH
if [ -n "$F_action" ]; then
  case "$F_action" in
# Show data from file and system
  showlog)
    echo "Content-type: text/html; charset=utf-8; Pragma: no-cache; Expires: Wednesday, 27-Dec-95 05:29:10 GMT"
    echo ""
    if [ -n "$F_raw" -a "$F_raw" = 1 ]; then
      tail /var/log/*
    else
      echo "<h1>Contents of all log files</h1>"
      echo "<pre>"
      tail /var/log/*
      echo "</pre>"
    fi
    ;;
# System Request
  reboot)
    getReturn 1234 "info" "Camera will reboot."
    /sbin/reboot
    ;;
  poweroff)
    getReturn 1234 "info" "Camera will safely power off."
    /sbin/poweroff
    ;;
  set_hostname)
    if [ -n "$F_hostname" ]; then
      if [ $(cat $CONFIGPATH/hostname.conf) != "$F_hostname" ]; then
        echo "$F_hostname" > $CONFIGPATH/hostname.conf
        hostname $F_hostname
        if [ $(cat $CONFIGPATH/hostname.conf) = "$F_hostname" ]; then
          getReturn 1234 "success" "The hostname has been changed successfully to '$F_hostname'."
        else
          getReturn 1234 "error" "An error occurred while changing the hostname."
        fi
      else
        getReturn 1234 "info" "The hostname is already set to '$F_hostname', so has not been changed."
      fi
    else
      getReturn 1234 "info" "The \\\"hostname\\\" parameter is empty, so has not been changed."
    fi
    ;;
  set_timezone)
    if [ -n "$F_tz" ]; then
      if [ $(cat /etc/TZ) != "$F_tz" ]; then
        echo "$F_tz" > /etc/TZ
        if [ $(cat /etc/TZ) = "$F_tz" ]; then
          $BINPATH/busybox ntpd -q -n -p time.google.com 2>&1
          getReturn 1234 "success" "The timezone has been changed successfully to '$F_tz'."
        else
          getReturn 1234 "error" "An error occurred while changing the timezone."
        fi
      else
        getReturn 1234 "info" "The timezone is already set to '$F_tz', so has not been changed."
      fi
    else
      getReturn 1234 "info" "The 'tz=[value]' parameter is empty, so has not been changed."
    fi
    ;;
  systeminfo)
    echo "Content-type: application/json; charset=utf-8; Pragma: no-cache; Expires: Wednesday, 27-Dec-95 05:29:10 GMT"
    echo ""

    echo "{
  \"code\": 123,
  \"status\": \"info\",
  \"description\": \"System information\",
  \"system\": {
    \"hostname\": \"$(cat $CONFIGPATH/hostname.conf)\",
    \"kernel\": \"$($BINPATH/busybox uname -r)\",
    \"uptime\": $(cat /proc/uptime | cut -d. -f1),
    \"cpu_avg\": $(cat /proc/loadavg | cut -d " " -f1),
    \"datetime\": {
      \"date\": \"$(date +'%Y-%m-%d')\",
      \"time\": \"$(date +'%T')\"
    },
    \"network\": {
      \"mac\": \"$(cat /params/config/.product_config | grep MAC | cut -c16-27 | sed 's/\(..\)/\1:/g;s/:$//')\",
      \"router\": {
        \"name\": \"$(iwgetid -r)\",
        \"mac\": \"$(iwgetid -r -a)\",
        \"ip\": \"$(ifconfig wlan0 | grep 'inet addr'| cut -d: -f2 | cut -d' ' -f1)\",
        \"channel\": $(iwgetid -r -c),
        \"freq\": \"$(iwgetid -r -f | cut -de -f1)\",
        \"rx\": $(ifconfig wlan0 | grep 'RX bytes' | cut -d: -f2 | cut -d' ' -f1),
        \"tx\": $(ifconfig wlan0 | grep 'TX bytes' | cut -d: -f3 | cut -d' ' -f1),
        \"signal\": $(cat /proc/net/wireless | tr -s ' ' $'\t' | grep wlan0: | cut -f4 | cut -d. -f1)
      }
    },
    \"disk_space\": {
      \"total\": $(df | tr -s ' ' $'\t' | grep /dev/mmcblk0p1 | grep /system/sdcard | cut -f2),
      \"used\": $(df | tr -s ' ' $'\t' | grep /dev/mmcblk0p1 | grep /system/sdcard | cut -f3),
      \"free\": $(df | tr -s ' ' $'\t' | grep /dev/mmcblk0p1 | grep /system/sdcard | cut -f4)
    },
    \"memory\": {
      \"total\": $(cat /proc/meminfo  | tr -s ' ' $'\t' | grep MemTotal: | cut -f2),
      \"free\": $(cat /proc/meminfo  | tr -s ' ' $'\t' | grep MemFree: | cut -f2),
      \"buffers\": $(cat /proc/meminfo  | tr -s ' ' $'\t' | grep Buffers: | cut -f2),
      \"cached\": $(cat /proc/meminfo  | tr -s ' ' $'\t' | grep Cached: | cut -f2 | head -1),
      \"swap\": {
        \"total\": $(cat /proc/meminfo  | tr -s ' ' $'\t' | grep SwapTotal: | cut -f2),
        \"free\": $(cat /proc/meminfo  | tr -s ' ' $'\t' | grep SwapFree: | cut -f2)
      }
    },
    \"motor\": {
      \"x\": $($MOTOR -d s | sed -n '1 p' | awk '{print $2}'),
      \"y\": $($MOTOR -d s | sed -n '2 p' | awk '{print $2}'),
      \"speed\": $($MOTOR -d s | sed -n '3 p' | awk '{print $2}')
    }
  }
}"
    ;;
# Control LED and IR
  blue_led_on)
    setGpio 38 1
    setGpio 39 0
    getReturn 1234 "success" "Blue LED is On."
    ;;
  blue_led_off)
    setGpio 39 1
    getReturn 1234 "success" "Blue LED is Off."
    ;;
  yellow_led_on)
    setGpio 38 0
    setGpio 39 1
    getReturn 1234 "success" "Yellow LED is On."
    ;;
  yellow_led_off)
    setGpio 38 1
    getReturn 1234 "success" "Yellow LED is Off."
    ;;
  ir_led_on)
    setGpio 49 0
    getReturn 1234 "success" "IR LED is On."
    ;;
  ir_led_off)
    setGpio 49 1
    getReturn 1234 "success" "IR LED is Off."
    ;;
  ir_cut_on)
    setGpio 25 1
    setGpio 26 0
    getReturn 1234 "success" "IR Filter is On."
    ;;
  ir_cut_off)
    setGpio 25 0
    setGpio 26 1
    getReturn 1234 "success" "IR Filter is Off."
    ;;
# Control Motor PTZ
  motor_stop)
    $BINPATH/motor -d s &>/dev/null &
    getReturn 1234 "success" "The motor on the camera has stopped."
    ;;
  motor_left)
    $BINPATH/motor -d l -s $F_ns &>/dev/null &
    getReturn 1234 "success" "The motor has moved the camera to the left for '$F_ns'ms."
    ;;
  motor_right)
    $BINPATH/motor -d r -s $F_ns &>/dev/null &
    getReturn 1234 "success" "The motor has moved the camera to the right for '$F_ns'ms."
    ;;
  motor_up)
    $BINPATH/motor -d u -s $F_ns &>/dev/null &
    getReturn 1234 "success" "The motor has moved the camera to the up for '$F_ns'ms."
    ;;
  motor_down)
    $BINPATH/motor -d d -s $F_ns &>/dev/null &
    getReturn 1234 "success" "The motor has moved the camera to the down for '$F_ns'ms."
    ;;
  motor_calibrate)
     $BINPATH/motor -d v -s 100 &>/dev/null &
     $BINPATH/motor -d h -s 100 &>/dev/null &
     getReturn 1234 "success" "Motor is calibration on vertical and horizontal."
  ;;
  motor_vcalibrate)
     $BINPATH/motor -d v -s 100 &>/dev/null &
     getReturn 1234 "success" "Motor is calibration on vertical."
  ;;
  motor_hcalibrate)
     $BINPATH/motor -d h -s 100 &>/dev/null &
     getReturn 1234 "success" "Motor is calibration on horizontal."
  ;;
# Control Audio
  audio_test)
    $BINPATH/audioplay /usr/share/notify/CN/init_ok.wav &
    getReturn 1234 "info" "Play test audio."
    ;;
  audio_record_start)
    $BINPATH/busybox nohup $BINPATH/ossrecord $SDPATH/test.wav &>/dev/null &
    getReturn 1234 "info" "Audio recording to the \"audio.wav\" file has been started."
  ;;
  audio_record_stop)
    killall ossrecord
    getReturn 1234 "success" "The \"ossrecord\" process was killed."
  ;;
# Control Video
  h264_record_start)
    $BINPATH/busybox nohup $BINPATH/h264Snap > $SDPATH/video.h264 &>/dev/null &
  ;;
  h264_record_stop)
  killall h264Snap
  getReturn 1234 "success" "The \"ossrecord\" process was killed."
  ;;
  h264_start)
    $BINPATH/busybox nohup $BINPATH/v4l2rtspserver-master -F 10 &>/dev/null &
    ;;
  mjpeg_start)
    $BINPATH/busybox nohup $BINPATH/v4l2rtspserver-master -fMJPG -F 10 &>/dev/null &
  ;;
  rtsp_stop)
    killall v4l2rtspserver-master
  ;;
  get_snaphot)
    if [ $F_raw == 1 ]; then
      $BINPATH/getimage > /run/snaphot.jpg
    else
      if [ `ps | grep v4l2rtspserver-master | grep -v grep | wc -l` -eq 1 ]; then
        PARAMS=" -v 0 -rtsp_transport tcp -y -i rtsp://0.0.0.0:8554/unicast -vframes 1"
        if [ -n $F_width -a -n $F_height -a $F_width -eq $F_width -a $F_height -eq $F_height ]; then PARAMS="$PARAMS -s $F_width"x"$F_height"; fi
        if [ $F_flip == 1 ]; then PARAMS="$PARAMS  -vf transpose=1,transpose=1"; fi
        if [ $F_nightvision == 1 ]; then PARAMS="$PARAMS -vf lutyuv=u=128:v=128"; fi
        PARAMS="$PARAMS -f image2 /run/snaphot.jpg"

        $BINPATH/busybox nohup $BINPATH/avconv $PARAMS
      else
  #      $BINPATH/getimage > /run/snaphot.jpg
  #      PARAMS=""
  #
  #      if [ $F_nightvision == 1 ]; then PARAMS="$PARAMS -n"; fi
  #      if [ $F_flip == 1 ]; then PARAMS="$PARAMS -r"; fi
  #      if [ -n $F_width -a $F_width -eq $F_width ]; then PARAMS="$PARAMS -W $F_width"; else PARAMS="$PARAMS -W 1920"; fi
  #      if [ -n $F_height -a $F_height -eq $F_height ]; then PARAMS="$PARAMS -H $F_height"; else PARAMS="$PARAMS -H 1080"; fi

  #      $BINPATH/v4l2rtspserver-master -fMJPG $PARAMS -O /stdout > /run/snaphot.jpg

        $BINPATH/busybox nohup $BINPATH/v4l2rtspserver-master -fMJPG -F 10 &>/dev/null &

        PARAMS=" -v 0 -rtsp_transport tcp -y -i rtsp://0.0.0.0:8554/unicast -vframes 1"
        if [ -n $F_width -a -n $F_height -a $F_width -eq $F_width -a $F_height -eq $F_height ]; then PARAMS="$PARAMS -s $F_width"x"$F_height"; fi
        if [ $F_flip == 1 ]; then PARAMS="$PARAMS  -vf transpose=1,transpose=1"; fi
        if [ $F_nightvision == 1 ]; then PARAMS="$PARAMS -vf lutyuv=u=128:v=128"; fi
        PARAMS="$PARAMS -f image2 /run/snaphot.jpg"

        $BINPATH/busybox nohup $BINPATH/avconv $PARAMS

        killall v4l2rtspserver-master
      fi
    fi

    if [ -e /run/snaphot.jpg ]; then
      if [ $F_json == 1 ]; then
        echo "Content-type: application/json; charset=utf-8; Pragma: no-cache; Expires: Wednesday, 27-Dec-95 05:29:10 GMT"
        echo ""
        echo "{
  \"code\": 123,
  \"status\": \"info\",
  \"description\": \"Take a snaphot.\",
  \"snaphot\": \"`cat /run/snaphot.jpg | $BINPATH/busybox base64 | tr -d '\n'`\"
}"
        rm /run/snaphot.jpg
      else
        echo "Content-type: image/jpg; charset=utf-8; Pragma: no-cache; Expires: Wednesday, 27-Dec-95 05:29:10 GMT"
        echo ""
        cat /run/snaphot.jpg
        rm /run/snaphot.jpg
      fi
    else
      getReturn 1234 "error" "An error occurred while taking snaphot."
    fi
  ;;
# Other
  check_light)
#    if [ `dd if=/dev/jz_adc_aux_0 count=10 | sed -e 's/[^\.]//g' | wc -m` -lt 30 ]; then
    if [ `dd if=/dev/jz_adc_aux_0 count=20 | sed -e 's/[^\.]//g' | wc -m` -lt 50 ]; then
      getReturn 1234 "info" "Light sensor say's Day"
    else
      getReturn 1234 "info" "Light sensor say's Night"
    fi
  ;;
  xiaomi_start)
    getReturn 1234 "info" "Official software will running."
    busybox insmod /driver/sinfo.ko  2>&1
    busybox rmmod sample_motor  2>&1
    $BINPATH/busybox nohup /system/bin/iCamera &  &>/dev/null &
  ;;
  send_picture_mail)
    $SDPATH/scripts/sendPictureMail.sh
    if [ $? == 0 ]; then
      getReturn 1234 "success" "sendPictureMail completed successfully"
    else
      getReturn 1234 "error" "sendPictureMail failed"
    fi
  ;;
  *)
  getReturn 1234 "error" "Unsupported command '$F_action'"
  ;;
  esac
  else
    echo "Content-type: text/html; charset=utf-8; Pragma: no-cache; Expires: Wednesday, 27-Dec-95 05:29:10 GMT"
    echo ""

    echo "<!DOCTYPE html>
    <html>
    <head>
    <title>Custom Software For Xiaomi Dafang ($VERSION)</title>
    <meta name=\"viewport\" content=\"width=device-width\">
    <link href='https://fonts.googleapis.com/css?family=Source+Sans+Pro:200,300,400,600,700,900,' rel='stylesheet' type='text/css'>
    <link href='https://fonts.googleapis.com/css?family=Fira+Sans:300,400,500,700' rel='stylesheet' type='text/css'>
    <style>

      html { line-height: 1.15; /* 1 */ -webkit-text-size-adjust: 100%; /* 2 */ } body { margin: 0; } h1 { font-size: 2em; margin: 0.67em 0; } hr { box-sizing: content-box; /* 1 */ height: 0; /* 1 */ overflow: visible; /* 2 */ } pre { font-family: monospace, monospace; /* 1 */ font-size: 1em; /* 2 */ } a { background-color: transparent; } abbr[title] { border-bottom: none; /* 1 */ text-decoration: underline; /* 2 */ text-decoration: underline dotted; /* 2 */ } b, strong { font-weight: bolder; } code, kbd, samp { font-family: monospace, monospace; /* 1 */ font-size: 1em; /* 2 */ } small { font-size: 80%; } sub, sup { font-size: 75%; line-height: 0; position: relative; vertical-align: baseline; } sub { bottom: -0.25em; } sup { top: -0.5em; } img { border-style: none; } button, input, optgroup, select, textarea { font-family: inherit; /* 1 */ font-size: 100%; /* 1 */ line-height: 1.15; /* 1 */ margin: 0; /* 2 */ } button, input { /* 1 */ overflow: visible; } button, select { /* 1 */ text-transform: none; } button, [type="button"], [type="reset"], [type="submit"] { -webkit-appearance: button; } button::-moz-focus-inner, [type="button"]::-moz-focus-inner, [type="reset"]::-moz-focus-inner, [type="submit"]::-moz-focus-inner { border-style: none; padding: 0; } button:-moz-focusring, [type="button"]:-moz-focusring, [type="reset"]:-moz-focusring, [type="submit"]:-moz-focusring { outline: 1px dotted ButtonText; } fieldset { padding: 0.35em 0.75em 0.625em; } legend { box-sizing: border-box; /* 1 */ color: inherit; /* 2 */ display: table; /* 1 */ max-width: 100%; /* 1 */ padding: 0; /* 3 */ white-space: normal; /* 1 */ } progress { vertical-align: baseline; } textarea { overflow: auto; } [type="checkbox"], [type="radio"] { box-sizing: border-box; /* 1 */ padding: 0; /* 2 */ } [type="number"]::-webkit-inner-spin-button, [type="number"]::-webkit-outer-spin-button { height: auto; } [type="search"] { -webkit-appearance: textfield; /* 1 */ outline-offset: -2px; /* 2 */ } [type="search"]::-webkit-search-decoration { -webkit-appearance: none; } ::-webkit-file-upload-button { -webkit-appearance: button; /* 1 */ font: inherit; /* 2 */ } details { display: block; } summary { display: list-item; } template { display: none; } [hidden] { display: none; }

      body {
        color: #393f57;
        font-size:100%;
        font-family: Source Sans Pro;
      }

      h1 {
        color: #00ab91;
        line-height:1.1;
            font-weight: 100;
      }

      h2 {
        line-height:1.1;
      }

      p {
        line-height:1.4;
      }

      a{
        color: #795548;
      }

      header .bars {
        display: block;
        height: 5px;
        margin: 0;
        overflow: hidden;
        position: fixed;
        text-align: center;
        top: 0;
        width: 100%;
      }
      header .bars ul {
        margin: 0;
        padding: 0;
      }
      header .bars ul li {
        display: block;
        float: left;
        height: 5px;
        overflow: hidden;
        width: 20%;
      }
      header .bars .cor-1 {
        background: #ED5565;
      }
      header .bars .cor-2 {
        background: #f59120;
      }
      header .bars .cor-3 {
        background: #FCBB42;
      }
      header .bars .cor-4 {
        background: #94c23d;
      }
      header .bars .cor-5 {
        background-color: #3498db;
      }

      header .header-title {
        background: #00ab91;
        height: 200px;
        color: #efefef;
        line-height: 200px;
        text-align: center;
        font-size: 40px;
      }

      section {
        margin:0 auto;
        padding-bottom:10px;
        max-width:600px;
      }

      section:first-child:last-child {
        padding-top:5%;
        padding-bottom:5%;
      }

      section.content-block {
        font-family: Fira Sans;
      }
      section.content-block p {
        font-weight:500;
      }

      footer {
        right: 0;
        bottom: 0;
        left: 0;
        padding: 1rem;
        background-color: #efefef;
        text-align: center;
      }
      footer a {
        text-decoration: none;
      }

      @media screen and (max-width: 960px) {
        header .bars {
          position: inherit;
        }
      }
    </style>
    </head>
    <body>
    <header>
      <div class=\"bars\">
        <ul>
          <li class=\"cor-1\"></li>
          <li class=\"cor-2\"></li>
          <li class=\"cor-3\"></li>
          <li class=\"cor-4\"></li>
          <li class=\"cor-5\"></li>
        </ul>
      </div>
      <div class=\"header-title\">
        Custom Software For Xiaomi Dafang
      </div>
    </header>
    <section class=\"content-block\">
      <h1>API Documentation</h1>
      <p>Please see API Documentation on <a href=\"https://kszere.gitbooks.io/xiaomi-dafang-api/content/\" target=\"_blank\">GitBook</a> for know what use this API.</p>
    </section>

    <section class=\"content-block\">
      <h1>Manual</h1>
      <p>Please read Manual on <a href=\"https://kszere.gitbooks.io/manual-for-xiaomi-dafang-api/content/\" target=\"_blank\">GitBook</a>.</p>
    </section>

    <section class=\"content-block\">
      <h1>Source Code</h1>
      <p>Available on <a href=\"https://github.com/kszere/Xiaomi-Dafang-API\" target=\"_blank\">GitHub</a>.</p>
      <p>You can report issue and suggest new function or contribute development.</p>
    </section>

    <footer>
    <a href=\"https://www.facebook.com/kszere/\" target=\"_blank\">KSZERE</a> 2018
    </footer>
    </body>
    </html>"
  fi


exit 0
