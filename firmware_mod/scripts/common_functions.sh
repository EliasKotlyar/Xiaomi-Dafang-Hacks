#!/bin/sh

# This file is supposed to bundle some frequently used functions
# so they can be easily improved in one place and be reused all over the place

# Initialize  gpio pin
init_gpio(){
  GPIOPIN=$1
  echo "$GPIOPIN" > /sys/class/gpio/export
  echo out > "/sys/class/gpio/gpio$GPIOPIN/direction"
  echo 0 > "/sys/class/gpio/gpio$GPIOPIN/active_low"
}

# Read a value from a gpio pin
getgpio(){
  GPIOPIN=$1
  cat /sys/class/gpio/gpio"$GPIOPIN"/value
}

# Write a value to gpio pin
setgpio() {
  GPIOPIN=$1
  echo "$2" > "/sys/class/gpio/gpio$GPIOPIN/value"
}

# Replace the old value of a config_key at the cfg_path with new_value
# Don't rewrite commented lines
rewrite_config(){
  cfg_path=$1
  cfg_key=$2
  new_value=$3
  sed -i -e "/\\s*#.*/!{/""$cfg_key""=/ s/=.*/=""$new_value""/}" "$cfg_path"
}

# Reboot the camera
reboot(){
  /sbin/reboot
}

# Control the blue led
blue_led(){
  case "$1" in
  on)
    setgpio 38 1
    setgpio 39 0
    ;;
  off)
    setgpio 39 1
    ;;
  status)
    status=$(getgpio 39)
    case $status in
      0)
        echo "ON"
        ;;
      1)
        echo "OFF"
      ;;
    esac
  esac
}

# Control the yellow led
yellow_led(){
  case "$1" in
  on)
    setgpio 38 0
    setgpio 39 1
    ;;
  off)
    setgpio 38 1
    ;;
  status)
    status=$(getgpio 38)
    case $status in
      0)
        echo "ON"
        ;;
      1)
        echo "OFF"
      ;;
    esac
  esac
}

# Control the infrared led
ir_led(){
  case "$1" in
  on)
    setgpio 49 0
    ;;
  off)
    setgpio 49 1
    ;;
  status)
    status=$(getgpio 49)
    case $status in
      0)
        echo "ON"
        ;;
      1)
        echo "OFF"
      ;;
    esac
  esac
}

# Control the infrared filter
ir_cut(){
  case "$1" in
  on)
    setgpio 25 0
    setgpio 26 1
    ;;
  off)
    setgpio 25 1
    setgpio 26 0
    ;;
  status)
    status=$(getgpio 25)
    case $status in
      0)
        echo "ON"
        ;;
      1)
        echo "OFF"
      ;;
    esac
  esac
}

# Calibrate and control the motor
# use like: motor up 100
motor (){
  if [ -z "$2" ]
  then
    steps=100
  else
    steps=$2
  fi
  case "$1" in
  up)
    /system/sdcard/bin/motor -d u -s "$steps"
    ;;
  down)
    /system/sdcard/bin/motor -d d -s "$steps"
    ;;
  left)
    /system/sdcard/bin/motor -d l -s "$steps"
    ;;
  right)
    /system/sdcard/bin/motor -d r -s "$steps"
    ;;
  vcalibrate)
    /system/sdcard/bin/motor -d v -s "$steps"
    ;;
  hcalibrate)
    /system/sdcard/bin/motor -d h -s "$steps"
    ;;
  status)
    if [ "$2" = "horizontal" ]
      then
        status=$(/system/sdcard/bin/motor -d u -s 0 | grep "x_")
        if echo "$status" | grep -q "x_min: 1" ; then
          echo "left_endstop"
        elif echo "$status" | grep -q "x_max: 1" ; then
          echo "right_endstop"
        else
          echo "$status" |grep "x_steps" | cut -f2- -d ' '
        fi
    else
        status=$(/system/sdcard/bin/motor -d u -s 0 | grep "y_")
        if echo "$status" | grep -q "y_min: 1" ; then
          echo "down_endstop"
        elif echo "$status" | grep -q "y_max: 1" ; then
          echo "up_endstop"
        else
          echo "$status" |grep "y_steps" | cut -f2- -d ' '
        fi
    fi
    ;;
  esac
}

# Read the light sensor
ldr(){
  case "$1" in
  status)
    brightness=$(dd if=/dev/jz_adc_aux_0 count=20 2> /dev/null |  sed -e 's/[^\.]//g' | wc -m)
    echo "$brightness"
  esac
}

# Control the RTSP h264 server
rtsp_h264_server(){
  case "$1" in
  on)
    /system/sdcard/controlscripts/rtsp-h264 start
    ;;
  off)
    /system/sdcard/controlscripts/rtsp-h264 stop
    ;;
  status)
    if /system/sdcard/controlscripts/rtsp-h264 status | grep -q "PID"
      then
        echo "ON"
    else
        echo "OFF"
    fi
    ;;
  esac
}

# Control the RTSP mjpeg server
rtsp_mjpeg_server(){
  case "$1" in
  on)
    /system/sdcard/controlscripts/rtsp-mjpeg start
    ;;
  off)
    /system/sdcard/controlscripts/rtsp-mjpeg stop
    ;;
  status)
    if /system/sdcard/controlscripts/rtsp-mjpeg status | grep -q "PID"
    then
        echo "ON"
    else
        echo "OFF"
    fi
    ;;
  esac
}

# Control the motion detection function
motion_detection(){
  case "$1" in
  on)
    /system/sdcard/bin/setconf -k m -v 4
    ;;
  off)
    /system/sdcard/bin/setconf -k m -v -1
    ;;
  status)
    status=$(/system/sdcard/bin/setconf -g m 2>/dev/null)
    case $status in
      -1)
        echo "OFF"
        ;;
      *)
        echo "ON"
        ;;
    esac
  esac
}

# Control the motion tracking function
motion_tracking(){
  case "$1" in
  on)
    /system/sdcard/bin/setconf -k t -v on
    ;;
  off)
    /system/sdcard/bin/setconf -k t -v off
    ;;
  status)
    status=$(/system/sdcard/bin/setconf -g t 2>/dev/null)
    case $status in
      true)
        echo "ON"
        ;;
      *)
        echo "OFF"
        ;;
    esac
  esac
}

# Control the night mode
night_mode(){
  case "$1" in
  on)
    ir_led on
    ir_cut off
    /system/sdcard/bin/setconf -k n -v 1
    ;;
  off)
    ir_led off
    ir_cut on
    /system/sdcard/bin/setconf -k n -v 0
    ;;
  status)
    status=$(/system/sdcard/bin/setconf -g n)
    case $status in
      0)
        echo "OFF"
        ;;
      1)
        echo "ON"
        ;;
    esac
  esac
}

# Control the auto night mode
auto_night_mode(){
  case "$1" in
    on)
      /system/sdcard/controlscripts/auto-night-detection start
      ;;
    off)
      /system/sdcard/controlscripts/auto-night-detection stop
      ;;
    status)
      if [ -f /run/auto-night-detection.pid ]; then
        echo "ON";
      else
        echo "OFF"
      fi
  esac
}
