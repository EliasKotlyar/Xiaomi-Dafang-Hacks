#!/bin/sh

# A very light-weight interface just for responsive ui to get states

source func.cgi

getgpio(){
  GPIOPIN=$1
  cat /sys/class/gpio/gpio"$GPIOPIN"/value
}

echo "Content-type: text"
echo ""

if [ -n "$F_cmd" ]; then
  case "$F_cmd" in
  blue_led)
    blue=$(getgpio 39)
    if [ "$blue" == "0" ]; then blue="on"; fi
    if [ "$blue" == "1" ]; then blue="off"; fi
    echo $blue
    ;;

  yellow_led)
    yellow=$(getgpio 38)
    if [ "$yellow" == "0" ]; then yellow="on"; fi
    if [ "$yellow" == "1" ]; then yellow="off"; fi
    echo $yellow
    ;;

  ir_led)
    ir_led=$(getgpio 49)
    if [ "$ir_led" == "0" ]; then ir_led="on"; fi
    if [ "$ir_led" == "1" ]; then ir_led="off"; fi
    echo $ir_led
    ;;

  ir_cut)
    ir_cut=$(getgpio 26)
    if [ "$ir_cut" == "1" ]; then ir_cut="on"; fi
    if [ "$ir_cut" == "0" ]; then ir_cut="off"; fi
    echo $ir_cut
    ;;

  rtsp_h264)
    if [ -f /run/v4l2rtspserver-master-h264.pid ];
      then rtsp_h264="on";
    else
      rtsp_h264="off";
    fi
    echo $rtsp_h264
    ;;

  rtsp_mjpeg)
    if [ -f /run/v4l2rtspserver-master-mjpeg.pid ];
      then rtsp_mjpeg="on";
    else
      rtsp_mjpeg="off";
    fi
    echo $rtsp_mjpeg
    ;;

  auto_night_detection)
    if [ -f /run/auto-night-detection.pid ];
      then auto_night_mode="on";
    else
      auto_night_mode="off";
    fi
    echo $auto_night_mode
    ;;

  mqtt_status)
    if [ -f /run/mqtt-status.pid ];
      then mqtt_status="on";
    else
      mqtt_status="off";
    fi
    echo $mqtt_status
    ;;

  mqtt_control)
    if [ -f /run/mqtt-control.pid ];
      then mqtt_control="on";
    else
      mqtt_control="off";
    fi
    echo $mqtt_control
    ;;

  sound_on_startup)
    if [ -f /system/sdcard/config/autostart/sound-on-startup ];
      then sound_on_startup="on";
    else
      sound_on_startup="off";
    fi
    echo $sound_on_startup
    ;;

  motion_detection)
    motion_sensitivity=`/system/sdcard/bin/setconf -g m 2>/dev/null`
    if [ "${motion_sensitivity}X" == "X" ];
      then motion_sensitivity="0"
    fi
    if test $motion_sensitivity -lt 0;
      then motion_detection="off";
    else
      motion_detection="on";
    fi
    echo $motion_detection
    ;;
  *)
    echo "Unsupported command '$F_cmd'"
    ;;
  esac
  fi

exit 0
