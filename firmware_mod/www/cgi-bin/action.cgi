#!/bin/sh

echo "Content-type: text/html"
echo ""

source func.cgi

setgpio(){
GPIOPIN=$1
echo $2 > /sys/class/gpio/gpio$GPIOPIN/value
}

echo "<br/>"
export LD_LIBRARY_PATH=/system/lib
export LD_LIBRARY_PATH=/thirdlib:$LD_LIBRARY_PATH
if [ -n "$F_cmd" ]; then
  case "$F_cmd" in
  showlog)
    echo "Contents of all log files:<br/>"
    echo "<pre>"
    tail /var/log/*
    echo "</pre>"
    ;;
  reboot)
    echo "Rebooting device...<br/>"
    /sbin/reboot
    ;;
  blue_led_on)
    setgpio 38 1
    setgpio 39 0
    ;;
  blue_led_off)
    setgpio 39 1
    ;;
  yellow_led_on)
    setgpio 38 0
    setgpio 39 1
    ;;
  yellow_led_off)
    setgpio 38 1
    ;;
  ir_led_on)
    setgpio 49 0
    ;;
  ir_led_off)
    setgpio 49 1
    ;;
  ir_cut_on)
    setgpio 25 1
    setgpio 26 0
    ;;
  ir_cut_off)
    setgpio 25 0
    setgpio 26 1
    ;;
  motor_left)
    /system/sdcard/bin/motor -d l -s 100
    ;;
  motor_right)
    /system/sdcard/bin/motor -d r -s 100
    ;;
  motor_up)
    /system/sdcard/bin/motor -d u -s 100
    ;;
  motor_down)
    /system/sdcard/bin/motor -d d -s 100
    ;;
  motor_vcalibrate)
     /system/sdcard/bin/motor -d v -s 100
  ;;
  motor_hcalibrate)
     /system/sdcard/bin/motor -d h -s 100
  ;;
  audio_test)
    /system/sdcard/bin/ossplay /usr/share/notify/CN/init_ok.wav
    ;;
  h264_start)
    /system/sdcard/bin/busybox nohup /system/sdcard/bin/v4l2rtspserver-master -S &>/dev/null &
    ;;
  mjpeg_start)
    /system/sdcard/bin/busybox nohup /system/sdcard/bin/v4l2rtspserver-master -fMJPG &>/dev/null &
  ;;
  xiaomi_start)
    busybox insmod /driver/sinfo.ko  2>&1
    busybox rmmod sample_motor  2>&1
    #/system/sdcard/bin/busybox insmod /driver/sinfo.ko
    #rmmod sample_motor
    #cd /
    /system/sdcard/bin/busybox nohup /system/bin/iCamera &  &>/dev/null &
  ;;
  rtsp_stop)
        killall v4l2rtspserver-master
    ;;
   settz)
    tz=$(printf '%b' "${F_tz//%/\\x}")
    if [ $(cat /etc/TZ) != "$tz" ]; then
    echo "Setting TZ to '$tz'...<br/>"
    echo "$tz" > /etc/TZ
    echo "Syncing time...<br/>"
    /system/sdcard/bin/busybox ntpd -q -n -p time.google.com 2>&1
    fi
    hst=$(printf '%b' "${F_hostname//%/\\x}")
    if [ $(cat /system/sdcard/config/hostname.conf) != "$hst" ]; then
    echo "Setting hostname to '$hst'...<br/>"
    echo "$hst" > /system/sdcard/config/hostname.conf
    hostname $hst
    fi
    if [ $? -eq 0 ]; then echo "<br/>Success<br/>"; else echo "<br/>Failed<br/>"; fi
    ;;
  *)
    echo "Unsupported command '$F_cmd'"
    ;;
  esac
  fi

echo "<hr/>"
echo "<button title='Return to status page' onClick=\"window.location.href='status.cgi'\">Back</button>"
