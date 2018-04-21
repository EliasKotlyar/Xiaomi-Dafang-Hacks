#!/bin/sh

# A very light-weight interface just for responsive ui to get states

source func.cgi
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

  rtsp_h264)
    if [ -f /run/v4l2rtspserver-master-h264.pid ];
      then rtsp_h264="ON";
    else
      rtsp_h264="OFF";
    fi
    echo $rtsp_h264
    ;;

  rtsp_mjpeg)
    if [ -f /run/v4l2rtspserver-master-mjpeg.pid ];
      then rtsp_mjpeg="ON";
    else
      rtsp_mjpeg="OFF";
    fi
    echo $rtsp_mjpeg
    ;;

  auto_night_detection)
    echo $(auto_night_mode status)
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

  *)
    echo "Unsupported command '$F_cmd'"
    ;;
  esac
  fi

exit 0
