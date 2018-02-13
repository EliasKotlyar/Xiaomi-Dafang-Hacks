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
    /system/sdcard/controlscripts/rtsp-h264-with-segmentation start
    ;;
  h264_noseg_start)
    /system/sdcard/controlscripts/rtsp-h264 start
    ;;


  mjpeg_start) 
     /system/sdcard/controlscripts/rtsp-mjpeg start
  ;;
  h264_nosegmentation_start)
  /system/sdcard/controlscripts/rtsp-h264 start
 ;;


  xiaomi_start)

    echo 1 > /sys/class/gpio/gpio39/value
    echo 39 > /sys/class/gpio/unexport
    #echo 49 > /sys/class/gpio/unexport
    killall v4l2rtspserver-master
    busybox insmod /driver/sinfo.ko  2>&1
    busybox rmmod sample_motor  2>&1
    #/system/sdcard/bin/busybox insmod /driver/sinfo.ko
    #rmmod sample_motor
    #cd /
    /system/init/app_init.sh &
  ;;

  rtsp_stop)
    /system/sdcard/controlscripts/rtsp-h264-with-segmentation stop
     /system/sdcard/controlscripts/rtsp-mjpeg stop
     /system/sdcard/controlscripts/rtsp-h264 stop
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
    
	osd)
	enabled=$(printf '%b' "${F_OSDenable}")
	position=$(printf '%b' "${F_Position}")
	osdtext=$(printf '%b' "${F_osdtext//%/\\x}")
	osdtext=$(echo $osdtext | sed -e "s/\+/_/g")
	osdtext=$(echo $osdtext | sed -e "s/$/ /g")
	if [ ! -z $enabled ]; then
		/system/sdcard/bin/setconf -k o -v "$osdtext"
		echo "OSD set"
	else
		echo "OSD removed"
		/system/sdcard/bin/setconf -k o -v ""
	fi
	;;
	
	setldravg)
	ldravg=´$(printf '%b' "${F_avg/%/\\x}")
	ldravg=$(echo $ldravg | sed "s/[^0-9]//g")
	echo AVG=$ldravg > /system/sdcard/config/ldr-average
	echo "Average set to $ldravg iterations."
	;;
	
    auto_night_mode_start)
	/system/sdcard/controlscripts/auto-night-detection start	
	;;
    auto_night_mode_stop)
        /system/sdcard/controlscripts/auto-night-detection stop
	;;
     toggle-rtsp-nightvision-on)
	/system/sdcard/bin/setconf -k n -v 1
	;;
     toggle-rtsp-nightvision-off)
     /system/sdcard/bin/setconf -k n -v 0
	;;
	 flip-on)
	/system/sdcard/bin/setconf -k f -v 1
	;;
     flip-off)
     /system/sdcard/bin/setconf -k f -v 0
	;;

   *)
    echo "Unsupported command '$F_cmd'"
    ;;
  esac
  fi

echo "<hr/>"
echo "<button title='Return to status page' onClick=\"window.location.href='status.cgi'\">Back</button>"
