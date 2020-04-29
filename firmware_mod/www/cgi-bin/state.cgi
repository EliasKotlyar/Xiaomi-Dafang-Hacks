#!/bin/sh

# A very light-weight interface just for responsive ui to get states

source ./func.cgi
source /system/sdcard/scripts/common_functions.sh


echo "Content-type: text"
echo "Pragma: no-cache"
echo "Cache-Control: max-age=0, no-store, no-cache"
echo ""

if [ -n "$F_cmd" ]; then
  case "$F_cmd" in
  blue_led)
    echo $(blue_led status)
    ;;

  yellow_led)
    echo $(yellow_led status)
    ;;

  ir_led)
    echo $(ir_led status)
    ;;

  ir_cut)
    echo $(ir_cut status)
    ;;

  night_mode)
    echo $(night_mode status)
    ;;

  rtsp_h264)
    echo $(rtsp_h264_server status)
    ;;

  rtsp_mjpeg)
    echo $(rtsp_mjpeg_server status)
    ;;

  auto_night_detection)
    echo $(auto_night_mode status)
    ;;
  auto_night_detection_mode)
    . /system/sdcard/config/autonight.conf 2> /dev/null
    echo $autonight_mode
    ;;
  mqtt_status)
    if [ -f /run/mqtt-status.pid ];
      then mqtt_status="ON";
    else
      mqtt_status="OFF";
    fi
    echo $mqtt_status
    ;;

  mqtt_control)
    if [ -f /run/mqtt-control.pid ];
      then mqtt_control="ON";
    else
      mqtt_control="OFF";
    fi
    echo $mqtt_control
    ;;

  sound_on_startup)
    if [ -f /system/sdcard/config/autostart/sound-on-startup ];
      then sound_on_startup="ON";
    else
      sound_on_startup="OFF";
    fi
    echo $sound_on_startup
    ;;

  motion_detection)
    echo $(motion_detection status)
    ;;

  motion_tracking)
    echo $(motion_tracking status)
    ;;

  motion_mail)
    . /system/sdcard/config/motion.conf 2> /dev/null
    if [ "$send_email" == "true" ]; then
      echo "ON"
    else
      echo "OFF"
    fi
    ;;

  motion_telegram)
    . /system/sdcard/config/motion.conf 2> /dev/null
    if [ "$send_telegram" == "true" ]; then
      echo "ON"
    else
      echo "OFF"
    fi
    ;;

  motion_led)
    . /system/sdcard/config/motion.conf 2> /dev/null
    if [ "$motion_trigger_led" == "true" ]; then
      echo "ON"
    else
      echo "OFF"
    fi
    ;;

  motion_snapshot)
    . /system/sdcard/config/motion.conf 2> /dev/null
    if [ "$save_snapshot" == "true" ]; then
      echo "ON"
    else
      echo "OFF"
    fi
    ;;

  motion_mqtt)
    . /system/sdcard/config/motion.conf 2> /dev/null
    if [ "$publish_mqtt_message" == "true" ]; then
      echo "ON"
    else
      echo "OFF"
    fi
    ;;

  motion_mqtt_snapshot)
    . /system/sdcard/config/motion.conf 2> /dev/null
    if [ "$publish_mqtt_snapshot" == "true" ]; then
      echo "ON"
    else
      echo "OFF"
    fi
    ;;

  motion_mqtt_video)
    . /system/sdcard/config/motion.conf 2> /dev/null
    if [ "$publish_mqtt_video" == "true" ]; then
      echo "ON"
    else
      echo "OFF"
    fi
    ;;

  hostname)
    echo $(hostname);
    ;;

  version)   
    if [ -s "/system/sdcard/VERSION" ]; then   
    V_BRANCH=$(/system/sdcard/bin/jq -r .branch /system/sdcard/VERSION)
    V_COMMIT=$(/system/sdcard/bin/jq -r .commit /system/sdcard/VERSION)
    echo "commit <b>${V_COMMIT}</b> from branch <b>${V_BRANCH}</b>"
    else                                    
       echo "Need to update to create a version file." 
    fi                                      
    ;; 

  *)
    echo "Unsupported command '$F_cmd'"
    ;;

  esac
  fi

exit 0
