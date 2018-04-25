#!/bin/sh

echo "Content-type: text/html"
echo "Pragma: no-cache"
echo "Cache-Control: max-age=0, no-store, no-cache"
echo ""

source func.cgi
source /system/sdcard/scripts/common_functions.sh

export LD_LIBRARY_PATH=/system/lib
export LD_LIBRARY_PATH=/thirdlib:$LD_LIBRARY_PATH
if [ -n "$F_cmd" ]; then
  if [ -z "$F_val" ]; then
    F_val=100
  fi
  case "$F_cmd" in
    showlog)
      echo "<pre>"
      case "${F_logname}" in
        "" | 1)
            echo "Summary of all log files:<br/>"
            tail /var/log/*
            ;;
        2)
            echo "Contents of dmesg<br/>"
            /bin/dmesg
            ;;
        3)
            echo "Contents of logcat<br/>"
            /system/bin/logcat -d
            ;;
        4)
          echo "Contents of v4l2rtspserver-master-h264.log<br/>"
          cat /tmp/v4l2rtspserver-master-h264.log
          ;;
      esac
      echo "</pre>"
      return
    ;;

    reboot)
      echo "Rebooting device..."
      /sbin/reboot
      return
    ;;
    shutdown)
      echo "Shutting down device.."
      /sbin/halt
      return
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
       #read ntp_serv.conf
       conf_ntp_srv=$(cat /system/sdcard/config/ntp_srv.conf)

      if [ $conf_ntp_srv != "$ntp_srv" ]; then
        echo "<p>Setting NTP Server to '$ntp_srv'...</p>"
        echo "$ntp_srv" > /system/sdcard/config/ntp_srv.conf
        echo "<p>Syncing time on '$ntp_srv'...</p>"
        if /system/sdcard/bin/busybox ntpd -q -n -p "$ntp_srv" > /dev/null 2>&1; then
          echo "<p>Success</p>"
        else
          echo "<p>Failed</p>"
        fi
      fi

      tz=$(printf '%b' "${F_tz//%/\\x}")
      if [ "$(cat /etc/TZ)" != "$tz" ]; then
        echo "<p>Setting TZ to '$tz'...</p>"
        echo "$tz" > /etc/TZ
        echo "<p>Syncing time...</p>"
        if /system/sdcard/bin/busybox ntpd -q -n -p "$ntp_srv" > /dev/null 2>&1; then
          echo "<p>Success</p>"
        else echo "<p>Failed</p>"
        fi
      fi
      hst=$(printf '%b' "${F_hostname//%/\\x}")
      if [ "$(cat /system/sdcard/config/hostname.conf)" != "$hst" ]; then
        echo "<p>Setting hostname to '$hst'...</p>"
        echo "$hst" > /system/sdcard/config/hostname.conf
        if hostname "$hst"; then
          echo "<p>Success</p>"
        else echo "<p>Failed</p>"
        fi
      fi
      return
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
      return
    ;;

    setldravg)
      ldravg=$(printf '%b' "${F_avg/%/\\x}")
      ldravg=$(echo "$ldravg" | sed "s/[^0-9]//g")
      echo AVG="$ldravg" > /system/sdcard/config/ldr-average.conf
      echo "Average set to $ldravg iterations."
      return
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

    set_video_size)
      video_size=$(echo "${F_video_size}"| sed -e 's/+/ /g')
      rewrite_config /system/sdcard/config/rtspserver.conf RTSPH264OPTS "\"-S $video_size\""
      rewrite_config /system/sdcard/config/rtspserver.conf RTSPMJPEGOPTS "\"-S $video_size\""
      echo "Video resolution set to $video_size<br/>"
      if [ "$(rtsp_h264_server status)" = "ON" ]; then
        echo "Restarting H264 RSTP server<br/>"
        rtsp_h264_server off
        rtsp_h264_server on
      fi
      if [ "$(rtsp_mjpeg_server status)" = "ON" ]; then
        echo "Restarting MJPEG RSTP server<br/>"
        rtsp_mjpeg_server off
        rtsp_mjpeg_server on
      fi
    ;;

    set_region_of_interest)
        rewrite_config /system/sdcard/config/motion.conf region_of_interest "${F_x0},${F_y0},${F_x1},${F_y1}"
        rewrite_config /system/sdcard/config/motion.conf motion_sensitivity "${F_motion_sensitivity}"
        rewrite_config /system/sdcard/config/motion.conf motion_indicator_color "${F_motion_indicator_color}"
        rewrite_config /system/sdcard/config/motion.conf motion_timeout "${F_motion_timeout}"
        if [ "${F_motion_tracking}X" == "X" ]
        then
            rewrite_config /system/sdcard/config/motion.conf motion_tracking off
             /system/sdcard/bin/setconf -k t -v off
        else
            rewrite_config /system/sdcard/config/motion.conf motion_tracking on
            /system/sdcard/bin/setconf -k t -v on
        fi

        # echo "region_of_interest=${F_x0},${F_y0},${F_x1},${F_y1}" >  /system/sdcard/config/motion.conf
        # echo "motion_sensitivity=${F_motion_sensitivity}" >>  /system/sdcard/config/motion.conf
        # echo "motion_indicator_color=${F_motion_indicator_color}" >>  /system/sdcard/config/motion.conf

        /system/sdcard/bin/setconf -k r -v ${F_x0},${F_y0},${F_x1},${F_y1}
        /system/sdcard/bin/setconf -k m -v ${F_motion_sensitivity}
        /system/sdcard/bin/setconf -k z -v ${F_motion_indicator_color}
        /system/sdcard/bin/setconf -k u -v ${F_motion_timeout}

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

                    # Set the socket option in order to restart easily the server (socket in use)
                    echo 1 > /proc/sys/net/ipv4/tcp_tw_recycle

                    sleep 2
                    cmdLine="/system/sdcard/bin/busybox nohup "${executable}${cmdLine} 2>/dev/null
                    ${cmdLine}  2>/dev/null >/dev/null &

            else
                    echo "<p>process v4l2rtspserver-master was not found</p>"
            fi
        fi

        echo "Motion Configuration done"
        return
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

    conf_timelapse)
      tlinterval=$(printf '%b' "${F_tlinterval/%/\\x}")
      tlinterval=$(echo "$tlinterval" | sed "s/[^0-9\.]//g")
      if [ "$tlinterval" ]; then
        rewrite_config /system/sdcard/config/timelapse.conf TIMELAPSE_INTERVAL "$tlinterval"
        echo "Timelapse interval set to $tlinterval seconds."
      else
        echo "Invalid timelapse interval"
      fi
      tlduration=$(printf '%b' "${F_tlduration/%/\\x}")
      tlduration=$(echo "$tlduration" | sed "s/[^0-9\.]//g")
      if [ "$tlduration" ]; then
        rewrite_config /system/sdcard/config/timelapse.conf TIMELAPSE_DURATION "$tlduration"
        echo "Timelapse duration set to $tlduration minutes."
      else
        echo "Invalid timelapse duration"
      fi
      return
    ;;

   *)
    echo "Unsupported command '$F_cmd'"
    ;;

  esac
fi

echo "<hr/>"
echo "<button title='Return to status page' onClick=\"window.location.href='status.cgi'\">Back</button>"
