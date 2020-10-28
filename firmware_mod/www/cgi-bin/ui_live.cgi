#!/bin/sh

# CGI file for live view

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
  status_all)
    echo "auto_night_mode:$(auto_night_mode status)"
    echo "ir_led:$(ir_led status)"
    echo "ir_cut:$(ir_cut status)"  
    echo "blue_led:$(blue_led status)"
    echo "yellow_led:$(yellow_led status)"
    echo "motion_detection:$(motion_detection status)"
    echo "motion_mail:$(motion_send_mail status)"
    echo "motion_telegram:$(motion_send_telegram status)"
    echo "motion_led:$(motion_led status)"
    echo "motion_snapshot:$(motion_snapshot status)"
    echo "motion_mqtt:$(motion_mqtt_publish status)"
    echo "motion_mqtt_snapshot:$(motion_snapshot status)"
    echo "motion_mqtt_video:$(motion_mqtt_video status)"
    ;;
  
  show_HWmodel)
		detect_model
		return
		;;
  hostname)
    echo $(hostname);
    ;;

  motor)
    if [ -z "$F_val" ]; then
      F_val=100
    fi
	  motor $F_move $F_val
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
  auto_night_mode)
    auto_night_mode $F_action
    ;;
  ir_led)
    ir_led $F_action
    ;;
  ir_cut)
     ir_cut $F_action
    ;;
  blue_led)
    blue_led $F_action
    ;;
  yellow_led)
    yellow_led $F_action
    ;;
  motion_detection)
    motion_detection $F_action
    ;;
  motion_mail)
    motion_send_mail $F_action
    ;;
  motion_telegram)
    motion_send_telegram $F_action
    ;;
  motion_led)
    motion_led $F_action
    ;;
  motion_snapshot)
    motion_snapshot $F_action
    ;;
  motion_mqtt)
    motion_mqtt_publish $F_action
    ;;
  motion_mqtt_snapshot)
    motion_mqtt_snapshot $F_action
    ;;
  motion_mqtt_video)
    motion_mqtt_video $F_action
    ;;
  recording)
    recording $F_action
    ;;
  flip)
    if [ $(/system/sdcard/bin/setconf -g f) == "0" ]; then
      /system/sdcard/bin/setconf -k f -v 1
    else 
      /system/sdcard/bin/setconf -k f -v 0
    fi
    ;;
  *)
    echo "Unsupported command '$F_cmd'"
    ;;

  esac
  fi

exit 0
