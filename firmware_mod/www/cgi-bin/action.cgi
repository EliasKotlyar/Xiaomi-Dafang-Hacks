#!/bin/sh

. /system/sdcard/www/cgi-bin/func.cgi
. /system/sdcard/scripts/common_functions.sh

export LD_LIBRARY_PATH=/system/lib
export LD_LIBRARY_PATH=/thirdlib:$LD_LIBRARY_PATH

echo "Content-type: text/html"
echo "Pragma: no-cache"
echo "Cache-Control: max-age=0, no-store, no-cache"
echo ""

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
          echo "Content of dmesg<br/>"
          /bin/dmesg
          ;;

        3)
          echo "Content of logcat<br/>"
          /system/bin/logcat -d
          ;;

        4)
          echo "Content of v4l2rtspserver-master.log<br/>"
          cat /tmp/v4l2rtspserver-master.log
          ;;

        5)
          echo "Content of update.log <br/>"
          cat /system/sdcard/log/update.log
          ;;

        6)
          echo "Process List <br/>"
          ps
          ;;

        7)
          echo "Mounts <br/>"
          mount
          ;;

      esac
      echo "</pre>"
      return
    ;;
    clearlog)
      echo "<pre>"
      case "${F_logname}" in
        "" | 1)
          echo "Summary of all log files cleared<br/>"
          for i in /var/log/*
          do
              echo -n "" > $i
          done
          ;;
        2)
          echo "Content of dmesg cleared<br/>"
          /bin/dmesg -c > /dev/null
          ;;
        3)
          echo "Content of logcat cleared<br/>"
          /system/bin/logcat -c
          ;;
        4)
          echo "Content of v4l2rtspserver-master.log cleared<br/>"
          echo -n "" > /tmp/v4l2rtspserver-master.log
          ;;
        5)
          echo "Content of update.log cleared <br/>"
          echo -n "" > /system/sdcard/log/update.log
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
      blue_led on
    ;;

    blue_led_off)
      blue_led off
    ;;

    yellow_led_on)
      yellow_led on
    ;;

    yellow_led_off)
      yellow_led off
    ;;

    ir_led_on)
      ir_led on
    ;;

    ir_led_off)
      ir_led off
    ;;

    ir_cut_on)
      ir_cut on
    ;;

    ir_cut_off)
      ir_cut off
    ;;

    motor_left)
      motor left $F_val
    ;;

    motor_right)
      motor right $F_val
    ;;

    motor_up)
      motor up $F_val
    ;;

    motor_down)
      motor down $F_val
    ;;

    motor_calibrate)
      motor reset_pos_count $F_val
    ;;

    motor_PTZ)
      /system/sdcard/scripts/PTZpresets.sh $F_x_axis $F_y_axis
    ;;

    audio_test)
      F_audioSource=$(printf '%b' "${F_audioSource//%/\\x}")
      if [ "$F_audioSource" == "" ]; then
        F_audioSource="/usr/share/notify/CN/init_ok.wav"
      fi
      /system/sdcard/bin/busybox nohup /system/sdcard/bin/audioplay $F_audioSource $F_audiotestVol >> "/var/log/update.log" &
      echo  "Play $F_audioSource at volume $F_audiotestVol"
      return
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

    rtsp_stop)
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

      timezone_name=$(printf '%b' "${F_timeZone//%/\\x}")
      if [ "$(cat /system/sdcard/config/timezone.conf)" != "$timezone_name" ]; then
        echo "<p>Setting time zone to '$timezone_name'...</p>"
        echo "$timezone_name" > /system/sdcard/config/timezone.conf
        # Set system timezone from timezone name
        set_timezone
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

    set_http_password)
      password=$(printf '%b' "${F_password//%/\\x}")
      echo "<p>Setting http password to : $password</p>"
      http_password "$password"
    ;;

    osd)
      enabled=$(printf '%b' "${F_OSDenable}")
      axis_enable=$(printf '%b' "${F_AXISenable}")
      position=$(printf '%b' "${F_Position}")
      osdtext=$(printf '%b' "${F_osdtext//%/\\x}")
      osdtext=$(echo "$osdtext" | sed -e "s/\\+/ /g")
      fontName=$(printf '%b' "${F_fontName//%/\\x}")
      fontName=$(echo "$fontName" | sed -e "s/\\+/ /g")

      if [ ! -z "$axis_enable" ];then
        echo "DISPLAY_AXIS=true" > /system/sdcard/config/osd.conf
        echo "DISPLAY_AXIS enable<br />"
      else
        echo "DISPLAY_AXIS=false" > /system/sdcard/config/osd.conf
        echo "DISPLAY_AXIS disable<br />"
      fi
      
      echo "OSD=\"${osdtext}\"" | sed -r 's/[ ]X=.*"/"/' >> /system/sdcard/config/osd.conf
      echo "OSD set<br />"

      if [ ! -z "$enabled" ]; then
        echo "ENABLE_OSD=true" >> /system/sdcard/config/osd.conf
        update_axis
        echo "OSD enabled"
      else
        echo "ENABLE_OSD=false" >> /system/sdcard/config/osd.conf
        echo "OSD disabled"
        /system/sdcard/bin/setconf -k o -v ""
      fi

      echo "COLOR=${F_color}" >> /system/sdcard/config/osd.conf
      /system/sdcard/bin/setconf -k c -v "${F_color}"

      echo "SIZE=${F_OSDSize}" >> /system/sdcard/config/osd.conf
      /system/sdcard/bin/setconf -k s -v "${F_OSDSize}"

      echo "POSY=${F_posy}" >> /system/sdcard/config/osd.conf
      /system/sdcard/bin/setconf -k x -v "${F_posy}"

      echo "FIXEDW=${F_fixedw}" >> /system/sdcard/config/osd.conf
      /system/sdcard/bin/setconf -k w -v "${F_fixedw}"

      echo "SPACE=${F_spacepixels}" >> /system/sdcard/config/osd.conf
      /system/sdcard/bin/setconf -k p -v "${F_spacepixels}"

      echo "FONTNAME=${fontName}" >> /system/sdcard/config/osd.conf
      /system/sdcard/bin/setconf -k e -v "${fontName}"
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
      rewrite_config /system/sdcard/config/rtspserver.conf FLIP "ON"
      /system/sdcard/bin/setconf -k f -v 1
    ;;

    flip-off)
      rewrite_config /system/sdcard/config/rtspserver.conf FLIP "OFF"
      /system/sdcard/bin/setconf -k f -v 0
    ;;

    motion_detection_on)
      motion_detection on
    ;;

    motion_detection_off)
      motion_detection off
    ;;
    
    snapshot)
      snapshot
    ;;

    set_video_size)
      video_size=$(echo "${F_video_size}"| sed -e 's/+/ /g')
      video_format=$(printf '%b' "${F_video_format/%/\\x}")
      brbitrate=$(printf '%b' "${F_brbitrate/%/\\x}")
      videopassword=$(printf '%b' "${F_videopassword//%/\\x}")
      videouser=$(printf '%b' "${F_videouser//%/\\x}")
      videoport=$(echo "${F_videoport}"| sed -e 's/+/ /g')
      frmRateDen=$(printf '%b' "${F_frmRateDen/%/\\x}")
      frmRateNum=$(printf '%b' "${F_frmRateNum/%/\\x}")

      rewrite_config /system/sdcard/config/rtspserver.conf RTSPH264OPTS "\"$video_size\""
      rewrite_config /system/sdcard/config/rtspserver.conf RTSPMJPEGOPTS "\"$video_size\""
      rewrite_config /system/sdcard/config/rtspserver.conf BITRATE "$brbitrate"
      rewrite_config /system/sdcard/config/rtspserver.conf VIDEOFORMAT "$video_format"
      rewrite_config /system/sdcard/config/rtspserver.conf USERNAME "$videouser"
      rewrite_config /system/sdcard/config/rtspserver.conf USERPASSWORD "$videopassword"
      rewrite_config /system/sdcard/config/rtspserver.conf PORT "$videoport"
      if [ "$frmRateDen" != "" ]; then
        rewrite_config /system/sdcard/config/rtspserver.conf FRAMERATE_DEN "$frmRateDen"
      fi
      if [ "$frmRateNum" != "" ]; then
        rewrite_config /system/sdcard/config/rtspserver.conf FRAMERATE_NUM "$frmRateNum"
      fi

      echo "Video resolution set to $video_size<br/>"
      echo "Bitrate set to $brbitrate<br/>"
      echo "FrameRate set to $frmRateDen/$frmRateNum <br/>"
      /system/sdcard/bin/setconf -k d -v "$frmRateNum,$frmRateDen" 2>/dev/null
      echo "Video format set to $video_format<br/>"

      if [ "$(rtsp_h264_server status)" = "ON" ]; then
        rtsp_h264_server off
        rtsp_h264_server on
      fi
      if [ "$(rtsp_mjpeg_server status)" = "ON" ]; then
        rtsp_mjpeg_server off
        rtsp_mjpeg_server on
      fi
      return
    ;;

    set_region_of_interest)
        rewrite_config /system/sdcard/config/motion.conf region_of_interest "${F_x0},${F_y0},${F_x1},${F_y1}"
        rewrite_config /system/sdcard/config/motion.conf motion_sensitivity "${F_motion_sensitivity}"
        rewrite_config /system/sdcard/config/motion.conf motion_indicator_color "${F_motion_indicator_color}"
        rewrite_config /system/sdcard/config/motion.conf motion_timeout "${F_motion_timeout}"
        if [ "${F_motion_tracking}X" == "X" ]; then
          rewrite_config /system/sdcard/config/motion.conf motion_tracking off
          /system/sdcard/bin/setconf -k t -v off
        else
          rewrite_config /system/sdcard/config/motion.conf motion_tracking on
          /system/sdcard/bin/setconf -k t -v on
        fi

        if [ "${F_motion_detection}" == "true" ]; then
          echo "enabled motion detection"
          motion_detection on
        else
          echo "disabled motion detection"
          motion_detection off
        fi

        /system/sdcard/bin/setconf -k r -v ${F_x0},${F_y0},${F_x1},${F_y1}
        /system/sdcard/bin/setconf -k m -v ${F_motion_sensitivity}
        /system/sdcard/bin/setconf -k z -v ${F_motion_indicator_color}
        /system/sdcard/bin/setconf -k u -v ${F_motion_timeout}

        # Changed the detection region, need to restart the server
        if [ ${F_restart_server} == "1" ]
        then
            if [ "$(rtsp_h264_server status)" == "ON" ]; then
                rtsp_h264_server off
                rtsp_h264_server on
            fi
            if [ "$(rtsp_mjpeg_server status)" == "ON" ]; then
                rtsp_mjpeg_server off
                rtsp_mjpeg_server on
            fi
        fi

        echo "Motion Configuration done"
        return
    ;;

    autonight_sw)
      if [ ! -f /system/sdcard/config/autonight.conf ]; then
        echo "-S" > /system/sdcard/config/autonight.conf
      fi
      current_setting=$(sed 's/-S *//g' /system/sdcard/config/autonight.conf)
      echo "-S" $current_setting > /system/sdcard/config/autonight.conf
    ;;

    autonight_hw)
      if [ -f /system/sdcard/config/autonight.conf ]; then
        sed -i 's/-S *//g' /system/sdcard/config/autonight.conf
      fi
    ;;

    get_sw_night_config)
      cat /system/sdcard/config/autonight.conf
      exit
    ;;

    save_sw_night_config)
      #This also enables software mode
      night_mode_conf=$(echo "${F_val}"| sed "s/+/ /g" | sed "s/%2C/,/g")
      echo $night_mode_conf > /system/sdcard/config/autonight.conf
      echo Saved $night_mode_conf
    ;;

    offDebug)
      /system/sdcard/controlscripts/debug-on-osd stop
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

    conf_audioin)
       audioinFormat=$(printf '%b' "${F_audioinFormat/%/\\x}")
       audioinBR=$(printf '%b' "${F_audioinBR/%/\\x}")
       audiooutBR=$(printf '%b' "${F_audiooutBR/%/\\x}")

       if [ "$audioinBR" == "" ]; then
            audioinBR="8000"
       fi
       if [ "$audiooutBR" == "" ]; then
           audioOutBR = audioinBR
       fi
       if [ "$audioinFormat" == "OPUS" ]; then
            audioOutBR="48000"
       fi
       if [ "$audioinFormat" == "PCM" ]; then
            audioOutBR = audioinBR
       fi
       if [ "$audioinFormat" == "PCMU" ]; then
           audioOutBR = audioinBR
       fi

       rewrite_config /system/sdcard/config/rtspserver.conf AUDIOFORMAT "$audioinFormat"
       rewrite_config /system/sdcard/config/rtspserver.conf AUDIOINBR "$audioinBR"
       rewrite_config /system/sdcard/config/rtspserver.conf AUDIOOUTBR "$audiooutBR"
       rewrite_config /system/sdcard/config/rtspserver.conf FILTER "$F_audioinFilter"
       rewrite_config /system/sdcard/config/rtspserver.conf HIGHPASSFILTER "$F_HFEnabled"
       rewrite_config /system/sdcard/config/rtspserver.conf AECFILTER "$F_AECEnabled"
       rewrite_config /system/sdcard/config/rtspserver.conf HWVOLUME "$F_audioinVol"
       rewrite_config /system/sdcard/config/rtspserver.conf SWVOLUME "-1"

       echo "Audio format $audioinFormat <br/>"
       echo "In audio bitrate $audioinBR <br/>"
       echo "Out audio bitrate $audiooutBR <br/>"
       echo "Filter $F_audioinFilter <br/>"
       echo "High Pass Filter $F_HFEnabled <br/>"
       echo "AEC Filter $F_AECEnabled <br/>"
       echo "Volume $F_audioinVol <br/>"
       /system/sdcard/bin/setconf -k q -v "$F_audioinFilter" 2>/dev/null
       /system/sdcard/bin/setconf -k l -v "$F_HFEnabled" 2>/dev/null
       /system/sdcard/bin/setconf -k a -v "$F_AECEnabled" 2>/dev/null
       /system/sdcard/bin/setconf -k h -v "$F_audioinVol" 2>/dev/null
       return
     ;;

     update)
        processId=$(ps | grep autoupdate.sh | grep -v grep)
        if [ "$processId" == "" ]
        then
            echo "===============" >> /system/sdcard/log/update.log
            date >> /var/log/update.log
            if [ "$F_login" != "" ]; then
                /system/sdcard/bin/busybox nohup /system/sdcard/autoupdate.sh -s -v -f -u $F_login  >> "/system/sdcard/log/update.log" &
            else
                /system/sdcard/bin/busybox nohup /system/sdcard/autoupdate.sh -s -v -f >> "/system/sdcard/log/update.log" &
            fi
            processId=$(ps | grep autoupdate.sh | grep -v grep)
        fi
        echo $processId
        return
      ;;

     show_updateProgress)
        processId=$(ps | grep autoupdate.sh | grep -v grep)
        if [ "$processId" == "" ]
        then
            echo -n -1
        else
            if [ -f /tmp/progress ] ; then
                cat /tmp/progress
            else
                echo -n 0
            fi
        fi
        return
        ;;

     motion_detection_mail_on)
         rewrite_config /system/sdcard/config/motion.conf send_email "true"
         return
         ;;

     motion_detection_mail_off)
          rewrite_config /system/sdcard/config/motion.conf send_email "false"
          return
          ;;

     motion_detection_telegram_on)
          rewrite_config /system/sdcard/config/motion.conf send_telegram "true"
          return
          ;;

     motion_detection_telegram_off)
          rewrite_config /system/sdcard/config/motion.conf send_telegram "false"
          return
          ;;

     motion_detection_led_on)
          rewrite_config /system/sdcard/config/motion.conf motion_trigger_led "true"
          return
          ;;

     motion_detection_led_off)
          rewrite_config /system/sdcard/config/motion.conf motion_trigger_led "false"
          return
          ;;

     motion_detection_snapshot_on)
          rewrite_config /system/sdcard/config/motion.conf save_snapshot "true"
          return
          ;;

     motion_detection_snapshot_off)
          rewrite_config /system/sdcard/config/motion.conf save_snapshot "false"
          return
          ;;

     motion_detection_mqtt_publish_on)
          rewrite_config /system/sdcard/config/motion.conf publish_mqtt_message "true"
          return
          ;;

     motion_detection_mqtt_publish_off)
          rewrite_config /system/sdcard/config/motion.conf publish_mqtt_message "false"
          return
          ;;

     motion_detection_mqtt_snapshot_on)
          rewrite_config /system/sdcard/config/motion.conf publish_mqtt_snapshot "true"
          return
          ;;

     motion_detection_mqtt_snapshot_off)
          rewrite_config /system/sdcard/config/motion.conf publish_mqtt_snapshot "false"
          return
          ;;

     *)
        echo "Unsupported command '$F_cmd'"
        ;;

  esac
fi

echo "<hr/>"
echo "<button title='Return to status page' onClick=\"window.location.href='status.cgi'\">Back</button>"
