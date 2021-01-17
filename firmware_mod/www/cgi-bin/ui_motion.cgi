#!/bin/sh

. /system/sdcard/www/cgi-bin/func.cgi
. /system/sdcard/scripts/common_functions.sh

export LD_LIBRARY_PATH=/system/lib
export LD_LIBRARY_PATH=/thirdlib:$LD_LIBRARY_PATH

echo "Content-type: text"
echo "Pragma: no-cache"
echo "Cache-Control: max-age=0, no-store, no-cache"
echo ""

if [ -n "$F_cmd" ]; then
  case "$F_cmd" in
  get_config)
    if [ ! -f "/system/sdcard/config/motion.conf" ]; then
      $(cp /system/sdcard/config/motion.conf.dist /system/sdcard/config/motion.conf)
    fi
    source /system/sdcard/config/motion.conf
    echo "currentRegions#:#${region_of_interest}"
    echo "motionSensitivity#:#${motion_sensitivity}"
    echo "motionIndicatorColor#:#${motion_indicator_color}"
    echo "motionDetection#:#${motion_detection}"
    echo "motionTimeout#:#${motion_timeout}"
    echo "motionTracking#:#${motion_tracking}"
    echo "saveSnapshot#:#${save_snapshot}"
    echo "maxSnaphotDays#:#${max_snapshot_days}"
    echo "maxVideoDays#:#${max_video_days}"
    echo "ftpSnapshot#:#${ftp_snapshot}"
    echo "ftpVideo#:#${ftp_video}"
    echo "ftpHost#:#${ftp_host}"
    echo "ftpPort#:#${ftp_port}"
    echo "ftpUsername#:#${ftp_username}"
    echo "ftpPassword#:#${ftp_password}"
    echo "ftpStillsDir#:#${ftp_stills_dir}"
    echo "ftpVideosDir#:#${ftp_videos_dir}"
    echo "smbSnapshot#:#${smb_snapshot}"
    echo "smbVideo#:#${smb_video}"
    echo "smbShare#:#${smb_share}"
    echo "smbUsername#:#${smb_username}"
    echo "smbPassword#:#${smb_password}"
    echo "smbStillsDir#:#${smb_stills_path}"
    echo "smbVideosDir#:#${smb_videos_path}"
    echo "motionTriggerLed#:#${motion_trigger_led}"
    echo "mqttMessage#:#${publish_mqtt_message}"
    echo "mqttSnapshot#:#${publish_mqtt_snapshot}"
    echo "mqttVideo#:#${publish_mqtt_video}"
    echo "sendEmail#:#${send_email}"
    echo "sendTelegram#:#${send_telegram}"
    echo "telegramAlertType#:#${telegram_alert_type}"
    echo "sendMatrix#:#${send_matrix}"
    
	;;
  save_config)
    if [ -n "${F_motionDetection+x}" ]; then
	     F_motionDetection=$(printf '%b' "${F_motionDetection//%/\\x}")
		 rewrite_config /system/sdcard/config/motion.conf motion_detection $F_motionDetection
		  echo "Motion detection set to $F_motionDetection<br/>"
	  fi
    if [ -n "${F_motionSensitivity+x}" ]; then
		F_motionSensitivity=$(printf '%b' "${F_motionSensitivity//%/\\x}")
	    rewrite_config /system/sdcard/config/motion.conf motion_sensitivity $F_motionSensitivity
		  echo "Motion sensitivity set to $F_motionSensitivity<br/>"
	  fi
    if [ -n "${F_motionIndicatorColor+x}" ]; then
	  F_motionIndicatorColor=$(printf '%b' "${F_motionIndicatorColor//%/\\x}")
	  color='white black red green blue cyan yellow purple'
      rewrite_config /system/sdcard/config/motion.conf motion_indicator_color $F_motionIndicatorColor
      if [ "$F_motionIndicatorColor" == "-1" ]; then
        echo "Motion color indicator is deactivated<br/>"
      else
        echo -n "Motion color indicator set to "
        echo -n $(echo $color | cut -d ' ' -f $(($F_motionIndicatorColor + 1)))
		    echo "<br />"
      fi 
	  fi
    if [ -n "${F_motionTracking+x}" ]; then
		F_motionTracking=$(printf '%b' "${F_motionTracking//%/\\x}")
	    rewrite_config /system/sdcard/config/motion.conf motion_tracking $F_motionTracking
		  echo "Motion tracking set to $F_motionTracking<br/>"
	  fi
    if [ -n "${F_motionTimeout+x}" ]; then
		F_motionTimeout=$(printf '%b' "${F_motionTimeout//%/\\x}")
	    rewrite_config /system/sdcard/config/motion.conf motion_timeout $F_motionTimeout
		  echo "Motion timeout set to $F_motionTimeout<br/>"
	  fi
    if [ -n "${F_saveSnaphot+x}" ]; then
		F_saveSnaphot=$(printf '%b' "${F_saveSnaphot//%/\\x}")
	    rewrite_config /system/sdcard/config/motion.conf save_snapshot $F_saveSnaphot
		  echo "Save snapshot set to $F_saveSnaphot<br/>"
	  fi
    if [ -n "${F_maxSnaphotDays+x}" ]; then
		F_maxSnaphotDays=$(printf '%b' "${F_maxSnaphotDays//%/\\x}")
	    rewrite_config /system/sdcard/config/motion.conf max_snapshot_days $F_maxSnaphotDays
		  echo "Maximun snapshot retention in days set to $F_maxSnaphotDays<br/>"
	  fi
    if [ -n "${F_saveVideo+x}" ]; then
		F_saveVideo=$(printf '%b' "${F_saveVideo//%/\\x}")
	    rewrite_config /system/sdcard/config/motion.conf save_video $F_saveVideo
		  echo "Save video set to $F_saveVideo<br/>"
	  fi
    if [ -n "${F_maxVideoDays+x}" ]; then
		F_maxVideoDays=$(printf '%b' "${F_maxVideoDays//%/\\x}")
	    rewrite_config /system/sdcard/config/motion.conf max_video_days $F_maxVideoDays
		  echo "Maximun video retention in days set to $F_maxVideoDays<br/>"
	  fi
        if [ -n "${F_smbSnapshot+x}" ]; then
		 F_smbSnapshot=$(printf '%b' "${F_smbSnapshot//%/\\x}")
	    rewrite_config /system/sdcard/config/motion.conf smb_snapshot $F_smbSnapshot
		  echo "Save snapshot to samba share set to $F_smbSnapshot<br/>"
	  fi
        if [ -n "${F_smbVideo+x}" ]; then
		F_smbVideo=$(printf '%b' "${F_smbVideo//%/\\x}")
	    rewrite_config /system/sdcard/config/motion.conf smb_video $F_smbVideo
		  echo "Save video to samba share set to $F_smbVideo<br/>"
	  fi
        if [ -n "${F_smbShare+x}" ]; then
		F_smbShare=$(printf '%b' "${F_smbShare//%/\\x}" | sed 's/\//\\\//g')
	    rewrite_config /system/sdcard/config/motion.conf smb_share "\"$F_smbShare\""
		  echo "Samba share set to $F_smbShare<br/>"
	  fi
        if [ -n "${F_smbUsername+x}" ]; then
		F_smbUsername=$(printf '%b' "${F_smbUsername//%/\\x}")
	    rewrite_config /system/sdcard/config/motion.conf smb_username "\"$F_smbUsername\""
		  echo "Samba username set to $F_smbUsername<br/>"
	  fi
        if [ -n "${F_smbPassword+x}" ]; then
		F_smbPassword=$(printf '%b' "${F_smbPassword//%/\\x}"  | sed 's/\//\\\//g')
	    rewrite_config /system/sdcard/config/motion.conf smb_password "\"$F_smbPassword\""
		  echo "Samba passward set<br/>"
	  fi
        if [ -n "${F_smbStillsDir+x}" ]; then
		F_smbStillsDir=$(printf '%b' "${F_smbStillsDir//%/\\x}" | sed 's/\//\\\//g')
	    rewrite_config /system/sdcard/config/motion.conf smb_stills_path "\"$F_smbStillsDir\""
		  echo "Samba snapshot destination directory set to $F_smbStillsDir<br/>"
	  fi
    if [ -n "${F_smbVideosDir+x}" ]; then
		F_smbVideosDir=$(printf '%b' "${F_smbVideosDir//%/\\x}" | sed 's/\//\\\//g')
	    rewrite_config /system/sdcard/config/motion.conf smb_videos_path "\"$F_smbVideosDir\""
		  echo "Samba video destination directory set to $F_smbVideosDir<br/>"
	  fi
    if [ -n "${F_ftpSnapshot+x}" ]; then
		F_ftpSnapshot=$(printf '%b' "${F_ftpSnapshot//%/\\x}")
	    rewrite_config /system/sdcard/config/motion.conf ftp_snapshot  $F_ftpSnapshot
		  echo "Save snapshot to FTP set to  set to $F_ftpSnapshot<br/>"
	  fi
    if [ -n "${F_ftpVideo+x}" ]; then
		F_ftpVideo=$(printf '%b' "${F_ftpVideo//%/\\x}")
	    rewrite_config /system/sdcard/config/motion.conf ftp_video $F_ftpVideo
		  echo "Save video to FTP set to $F_ftpVideo<br/>"
	  fi
    if [ -n "${F_ftpHost+x}" ]; then
		F_ftpHost=$(printf '%b' "${F_ftpHost//%/\\x}")
	    rewrite_config /system/sdcard/config/motion.conf ftp_host "\"$F_ftpHost\""
		  echo "FTP Host set to $F_ftpHost<br/>"
	  fi
    if [ -n "${F_ftpPort+x}" ]; then
		F_ftpPort=$(printf '%b' "${F_ftpPort//%/\\x}")
	    rewrite_config /system/sdcard/config/motion.conf ftp_port $F_ftpPort
		  echo "FTP Port set to $F_ftpPort<br/>"
	  fi
    if [ -n "${F_ftpUsername+x}" ]; then
		F_ftpUsername=$(printf '%b' "${F_ftpUsername//%/\\x}")
	    rewrite_config /system/sdcard/config/motion.conf ftp_username "\"$F_ftpUsername\""
		  echo "FTP username set to $F_ftpUsername<br/>"
	  fi
    if [ -n "${F_ftpPassword+x}" ]; then
		  F_ftpPassword=$(printf '%b' "${F_ftpPassword//%/\\x}" | sed 's/\//\\\//g')
	      rewrite_config /system/sdcard/config/motion.conf ftp_password "\"$F_ftpPassword\""
		  echo "FTP password set<br/>"
	  fi
    if [ -n "${F_ftpStillsDir+x}" ]; then
		F_ftpStillsDir=$(printf '%b' "${F_ftpStillsDir//%/\\x}"  | sed 's/\//\\\//g')
	    rewrite_config /system/sdcard/config/motion.conf ftp_stills_dir "\"$F_ftpStillsDir\""
		  echo "FTP snapshots directory set to $F_ftpStillsDir<br/>"
	  fi
    if [ -n "${F_ftpVideosDir+x}" ]; then
		F_ftpVideosDir=$(printf '%b' "${F_ftpVideosDir//%/\\x}"  | sed 's/\//\\\//g')
	    rewrite_config /system/sdcard/config/motion.conf ftp_videos_dir "\"$F_ftpVideosDir\""
		echo "FTP videos directory set to $F_ftpVideosDir<br/>"
	  fi
    if [ -n "${F_motionTriggerLed+x}" ]; then
		F_motionTriggerLed=$(printf '%b' "${F_motionTriggerLed//%/\\x}")
	    rewrite_config /system/sdcard/config/motion.conf motion_trigger_led $F_motionTriggerLed
		  echo "Motion trigger led set to $F_motionTriggerLed<br/>"
	  fi
    if [ -n "${F_mqttMessage+x}" ]; then
	    F_mqttMessage=$(printf '%b' "${F_mqttMessage//%/\\x}")
	    rewrite_config /system/sdcard/config/motion.conf publish_mqtt_message $F_mqttMessage
		  echo "MQTT publish message on motion set to $F_mqttMessage<br/>"
	  fi
    if [ -n "${F_mqttSnapshot+x}" ]; then
	    F_mqttSnapshot=$(printf '%b' "${F_mqttSnapshot//%/\\x}")
	    rewrite_config /system/sdcard/config/motion.conf publish_mqtt_snapshot $F_mqttSnapshot
		  echo "MQTT publish image on motion set to $F_mqttSnapshot<br/>"
	  fi
    if [ -n "${F_mqttVideo+x}" ]; then
	    F_mqttVideo=$(printf '%b' "${F_mqttVideo//%/\\x}")
	    rewrite_config /system/sdcard/config/motion.conf publish_mqtt_video $F_mqttVideo
		  echo "MQTT publish video on motion set to $F_mqttVideo<br/>"
	  fi
    if [ -n "${F_sendEmail+x}" ]; then
		F_sendEmail=$(printf '%b' "${F_sendEmail//%/\\x}")
	    rewrite_config /system/sdcard/config/motion.conf send_email $F_sendEmail
		  echo "Send mail on motion set to $F_sendEmail<br/>"
	  fi
    if [ -n "${F_sendTelegram+x}" ]; then
	    F_sendTelegram=$(printf '%b' "${F_sendTelegram//%/\\x}")
	    rewrite_config /system/sdcard/config/motion.conf send_telegram $F_sendTelegram
		  echo "Send Telegram on motion set to $F_sendTelegram<br/>"
	  fi
    if [ -n "${F_telegramAlertType+x}" ]; then
	    F_telegramAlertType=$(printf '%b' "${F_telegramAlertType//%/\\x}")
	    rewrite_config /system/sdcard/config/motion.conf telegram_alert_type $F_telegramAlertType
		  echo "Telegram alert type set to $F_telegramAlertType<br/>"
	  fi
    if [ -n "${F_sendMatrix+x}" ]; then
		F_sendMatrix=$(printf '%b' "${F_sendMatrix//%/\\x}")
	    rewrite_config /system/sdcard/config/motion.conf send_matrix $F_sendMatrix
		  echo "Send Matrix on motion set to $F_sendMatrix<br/>"
	  fi
    if [ -n "${F_regions+x}" ]; then
	  F_regions=$(printf '%b' "${F_regions//%/\\x}")
	    rewrite_config /system/sdcard/config/motion.conf region_of_interest $F_regions
		  echo "Regions set to $F_regions<br/>"
	  fi
    if [ "$(rtsp_server status)" = "ON" ]; then
	    echo "Restarting rtsp server"
	    rtsp_server off
	    rtsp__server on
	  fi
    ;;
  *)
    echo "Unsupported command '$F_cmd'"
    ;;

  esac
  fi

exit 0

