#!/bin/sh

echo "Content-type: text/html"
echo ""

source func.cgi
source /system/sdcard/scripts/common_functions.sh

echo "<br/>"
export LD_LIBRARY_PATH=/system/lib
export LD_LIBRARY_PATH=/thirdlib:$LD_LIBRARY_PATH
if [ -n "$F_cmd" ]; then
  if [ -z "$F_val" ]; then
    F_val=100
  fi
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
      setgpio 25 0
      setgpio 26 1
    ;;

    ir_cut_off)
      setgpio 25 1
      setgpio 26 0
    ;;

    motor_left)
      /system/sdcard/bin/motor -d l -s $F_val
    ;;

    motor_right)
      /system/sdcard/bin/motor -d r -s $F_val
    ;;

    motor_up)
      /system/sdcard/bin/motor -d u -s $F_val
    ;;

    motor_down)
      /system/sdcard/bin/motor -d d -s $F_val
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
      /system/sdcard/controlscripts/rtsp-h264 start
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
      killall v4l2rtspserver-master
      busybox insmod /driver/sinfo.ko  2>&1
      busybox rmmod sample_motor  2>&1
      /system/init/app_init.sh &
    ;;

    rtsp_stop)
      /system/sdcard/controlscripts/rtsp-h264-with-segmentation stop
       /system/sdcard/controlscripts/rtsp-mjpeg stop
       /system/sdcard/controlscripts/rtsp-h264 stop
    ;;
    settz)
	
	ntp_srv=$(printf '%b' "${F_ntp_srv//%/\\x}")
	
	#lecture fichier ntp_serv.conf
	conf_ntp_srv=$(cat /system/sdcard/config/ntp_srv.conf)

    if [ $conf_ntp_srv != "$ntp_srv" ]; then
    echo "Setting NTP Server to '$ntp_srv'...<br/>"
    echo "$ntp_srv" > /system/sdcard/config/ntp_srv.conf
    echo "Syncing time on '$ntp_srv'...<br/>"
        if [ "$(/system/sdcard/bin/busybox ntpd -q -n -p $ntp_srv 2>&1)" -eq 0 ]; then
          echo "<br/>Success<br/>"
        else echo "<br/>Failed<br/>"
		fi
    fi

	#lecture fichier ntp_serv.conf
	conf_ntp_srv=$(cat /system/sdcard/config/ntp_srv.conf)

	tz=$(printf '%b' "${F_tz//%/\\x}")
      if [ "$(cat /etc/TZ)" != "$tz" ]; then
        echo "Setting TZ to '$tz'...<br/>"
        echo "$tz" > /etc/TZ
        echo "Syncing time...<br/>"
        if [ "$(/system/sdcard/bin/busybox ntpd -q -n -p $conf_ntp_srv 2>&1)" -eq 0 ]; then
          echo "<br/>Success<br/>"
        else echo "<br/>Failed<br/>"
        fi
      fi
      hst=$(printf '%b' "${F_hostname//%/\\x}")
      if [ "$(cat /system/sdcard/config/hostname.conf)" != "$hst" ]; then
        echo "Setting hostname to '$hst'...<br/>"
        echo "$hst" > /system/sdcard/config/hostname.conf
        if [ "$(hostname "$hst")" -eq 0 ]; then
          echo "<br/>Success<br/>"
        else echo "<br/>Failed<br/>"
        fi
      fi

    ;;

    osd)
      enabled=$(printf '%b' "${F_OSDenable}")
      position=$(printf '%b' "${F_Position}")
      osdtext=$(printf '%b' "${F_osdtext//%/\\x}")
      osdtext=$(echo "$osdtext" | sed -e "s/\\+/ /g")

      if [ ! -z "$enabled" ]; then
        /system/sdcard/bin/setconf -k o -v "$osdtext"
        echo "OSD=\"${osdtext}\"" > /system/sdcard/config/osd
        echo "OSD set"
      else
        echo "OSD removed"
        /system/sdcard/bin/setconf -k o -v ""
        echo "OSD=\"\" " > /system/sdcard/config/osd
      fi

      echo "COLOR=${F_color}" >> /system/sdcard/config/osd
      /system/sdcard/bin/setconf -k c -v "${F_color}"

      echo "SIZE=${F_size}" >> /system/sdcard/config/osd
      /system/sdcard/bin/setconf -k s -v "${F_size}"

      echo "POSY=${F_posy}" >> /system/sdcard/config/osd
      /system/sdcard/bin/setconf -k x -v "${F_posy}"

      echo "FIXEDW=${F_fixedw}" >> /system/sdcard/config/osd
      /system/sdcard/bin/setconf -k w -v "${F_fixedw}"

      echo "SPACE=${F_spacepixels}" >> /system/sdcard/config/osd
      /system/sdcard/bin/setconf -k p -v "${F_spacepixels}"
    ;;

    setldravg)
      ldravg=$(printf '%b' "${F_avg/%/\\x}")
      ldravg=$(echo "$ldravg" | sed "s/[^0-9]//g")
      echo AVG="$ldravg" > /system/sdcard/config/ldr-average
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

    motion_detection_on)
      /system/sdcard/bin/setconf -k m -v 4
    ;;

    motion_detection_off)
      /system/sdcard/bin/setconf -k m -v -1
    ;;

    set_region_of_interest)
        rewrite_config /system/sdcard/config/motion.conf region_of_interest "${F_x0},${F_y0},${F_x1},${F_y1}"
        rewrite_config /system/sdcard/config/motion.conf motion_sensitivity "${F_motion_sensitivity}"
        rewrite_config /system/sdcard/config/motion.conf motion_indicator_color "${F_motion_indicator_color}"

        # echo "region_of_interest=${F_x0},${F_y0},${F_x1},${F_y1}" >  /system/sdcard/config/motion.conf
        # echo "motion_sensitivity=${F_motion_sensitivity}" >>  /system/sdcard/config/motion.conf
        # echo "motion_indicator_color=${F_motion_indicator_color}" >>  /system/sdcard/config/motion.conf

        /system/sdcard/bin/setconf -k r -v ${F_x0},${F_y0},${F_x1},${F_y1}
        /system/sdcard/bin/setconf -k m -v ${F_motion_sensitivity}
        /system/sdcard/bin/setconf -k z -v ${F_motion_indicator_color}

        # Changed the detection region, need to restart the server
        if [ ${F_restart_server} == "1" ]
        then
            processName="v4l2rtspserver-master"
            #get the process pid
            processId=`ps | grep ${processName} | grep -v grep | awk '{ printf $1 }'`
            if [ "${processId}X" != "X" ]
            then
                    #found the process, now get the full path and the parameters in order to restart it
                    executable=`ls -l /proc/${processId}/exe | awk '{print $NF}'`
                    cmdLine=`tr '\0' ' ' < /proc/${processId}/cmdline | awk '{$1=""}1'`

                    kill ${processId} 2>/dev/null
                    sleep 2
                    cmdLine="/system/sdcard/bin/busybox nohup "${executable}${cmdLine} 2>/dev/null
                    ${cmdLine} &>/dev/null

            else
                    echo "process v4l2rtspserver-master was not found"
            fi
        fi

        echo "Motion Configuration done"
        echo "<BR>"
        echo "<button title='Return to motion configuration page' onClick=\"window.location.href='/configmotion.html'\">Back to motion configuration</button>"
    ;;
    offDebug)
        /system/sdcard/controlscripts/debug-on-osd stop
        if [ -f /system/sdcard/controlscripts/configureOsd ]; then
            source /system/sdcard/controlscripts/configureOsd
        fi

    ;;
    onDebug)
        /system/sdcard/controlscripts/debug-on-osd start
    ;;

   *)
    echo "Unsupported command '$F_cmd'"
    ;;

  esac
fi

echo "<hr/>"
echo "<button title='Return to status page' onClick=\"window.location.href='status.cgi'\">Back</button>"
