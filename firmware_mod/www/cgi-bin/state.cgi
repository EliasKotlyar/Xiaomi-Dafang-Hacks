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
  all)
    echo "auto_night_mode:$(auto_night_mode status)"
    if [ -f /system/sdcard/config/autostart/sound-on-startup ]; then 
      echo "sound_on_startup:ON"
    else
      echo "sound_on_startup:OFF"
    fi
    echo "ir_led:$(ir_led status)"
    echo "ir_cut:$(ir_cut status)"  
    echo "blue_led:$(blue_led status)"
    echo "yellow_led:$(yellow_led status)"
    echo "motion_detection:$(motion_detection status)"
    if [ get_config "/system/sdcard/config/motion.conf" "send_email" ] ; then
        echo "motion_mail:ON"
    else
        echo "motion_mail:OFF"
    fi
    if [ get_config "/system/sdcard/config/motion.conf" "send_telegram" ]; then
        echo "motion_telegram:ON"
    else
        echo "motion_telegram:OFF"
    fi
    if [ get_config "/system/sdcard/config/motion.conf" "motion_trigger_led" ]; then
        echo "motion_led:ON"
    else
        echo "motion_led:OFF"
    fi
    if [ get_config "/system/sdcard/config/motion.conf" "save_snapshot" ]; then
        echo "motion_snapshot:ON"
    else
        echo "motion_snapshot:OFF"
    fi
    if [ get_config "/system/sdcard/config/motion.conf" "publish_mqtt_message" ]; then
        echo "motion_mqtt:ON"
    else
        echo "motion_mqtt:OFF"
    fi
    if [ get_config "/system/sdcard/config/motion.conf" "publish_mqtt_snapshot" ]; then
        echo "motion_mqtt_snapshot:ON"
    else
        echo "motion_mqtt_snapshot:OFF"
    fi
    if [ get_config "/system/sdcard/config/motion.conf" "publish_mqtt_video" ]; then
        echo "motion_mqtt_video:ON"
    else
        echo "motion_mqtt_video:OFF"
    fi
    ;;
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

  rtsp)
    echo $(rtsp_server status)
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
    echo "commit <b>${V_COMMIT}</b> from the <b>${V_BRANCH}</b> branch"
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
