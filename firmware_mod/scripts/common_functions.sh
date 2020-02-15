#!/bin/sh

# This file is supposed to bundle some frequently used functions
# so they can be easily improved in one place and be reused all over the place

include () {
    [[ -f "$1" ]] && source "$1"
}
# Set motor range
MAX_X=2600
MAX_Y=700
MIN_X=0
MIN_Y=0
STEP=100

# Try to detect hardware model
detect_model(){
  if [ -f /driver/8189es.ko ]; then
    # Its a DaFang
    echo "Xiaomi Dafang"
  elif [ -f /driver/8189fs.ko ]; then
    # Its a XiaoFang T20
    echo "Xiaomi Xiaofang 1S"
  else
    # Its a Wyzecam V2
    echo "Wyzecam V2"
  fi
}
# Initialize  gpio pin
init_gpio(){
  GPIOPIN=$1
  echo "$GPIOPIN" > /sys/class/gpio/export
  case $2 in
    in)
      echo "in" > "/sys/class/gpio/gpio$GPIOPIN/direction"
      ;;
    *)
      echo "out" > "/sys/class/gpio/gpio$GPIOPIN/direction"
      ;;
  esac
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

# Get value for a key in a config_file
# ignore commented lines
get_config(){
  cfg_path=$1
  cfg_key=$2
  grep -v '^[[:space:]]*#' "$1"  | grep "$2" | cut -d "=" -f2
}

# Replace the old value of a config_key at the cfg_path with new_value
# Don't rewrite commented lines
rewrite_config(){
  cfg_path=$1
  cfg_key=$2
  new_value=$3

  # Check if the value exists (without comment), if not add it to the file
  $(grep -v '^[[:space:]]*#' "$1"  | grep -q "$2")
  ret="$?"
  if [ "$ret" == "1" ] ; then
      echo "$2=$3" >> $1
  else
        sed -i -e "/\\s*#.*/!{/""$cfg_key""=/ s/=.*/=""$new_value""/}" "$cfg_path"
  fi
}

# Control the blue led
blue_led(){
  case "$1" in
  on)
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
    sleep 1
    setgpio 26 0
    echo "1" > /var/run/ircut
    ;;
  off)
    setgpio 26 0
    setgpio 25 1
    sleep 1
    setgpio 25 0
    echo "0" > /var/run/ircut
    ;;
  status)
    status=$(cat /var/run/ircut)
    case $status in
      1)
        echo "ON"
        ;;
      0)
        echo "OFF"
      ;;
    esac
  esac
}

# Calibrate and control the motor
# use like: motor up 100
motor(){
  if [ -z "$2" ]
  then
    steps=$STEP
  else
    steps=$2
  fi
  case "$1" in
  up)
    /system/sdcard/bin/motor -d u -s "$steps"
    update_motor_pos "$steps"
    ;;
  down)
    /system/sdcard/bin/motor -d d -s "$steps"
    update_motor_pos "$steps"
    ;;
  left)
    /system/sdcard/bin/motor -d l -s "$steps"
    update_motor_pos "$steps"
    ;;
  right)
    /system/sdcard/bin/motor -d r -s "$steps"
    update_motor_pos "$steps"
    ;;
  reset_pos_count)
    /system/sdcard/bin/motor -d v -s "$steps"
    update_motor_pos "$steps"
    ;;
  status)
    if [ "$2" = "horizontal" ]; then
        /system/sdcard/bin/motor -d u -s 0 | grep "x:" | awk  '{print $2}'
    else
        /system/sdcard/bin/motor -d u -s 0 | grep "y:" | awk  '{print $2}'
    fi
    ;;
  esac

}

update_motor_pos(){
  # Waiting for the motor to run.
  SLEEP_NUM=$(awk -v a="$1" 'BEGIN{printf ("%f",a*1.3/1000)}')
  sleep ${SLEEP_NUM//-/}
  # Display AXIS to OSD
  update_axis
}

# Read the hw light sensor (hw in mqtt.conf)
ldr(){
  case "$1" in
  status)
    brightness=$(dd if=/dev/jz_adc_aux_0 count=20 2> /dev/null |  sed -e 's/[^\.]//g' | wc -m)
    echo "$brightness"
  esac
}

# Read the virtual light sensor (virtual in mqtt.conf)
exposure(){
  case "$1" in
  status)
    isp_exposure=$(grep 'ISP exposure log2 id:' /proc/jz/isp/isp_info  | sed 's/^.*: //')
    echo "$isp_exposure"
  esac
}

# Control the http server
http_server(){
  case "$1" in
  on)
    /system/sdcard/bin/lighttpd -f /system/sdcard/config/lighttpd.conf
    ;;
  off)
    killall lighttpd.bin
    ;;
  restart)
    killall lighttpd.bin
    /system/sdcard/bin/lighttpd -f /system/sdcard/config/lighttpd.conf
    ;;
  status)
    if pgrep lighttpd.bin &> /dev/null
      then
        echo "ON"
    else
        echo "OFF"
    fi
    ;;
  esac
}

# Set a new http password
http_password(){
  user="root" # by default root until we have proper user management
  realm="all" # realm is defined in the lightppd.conf
  pass=$1
  hash=$(echo -n "$user:$realm:$pass" | md5sum | cut -b -32)
  echo "$user:$realm:$hash" > /system/sdcard/config/lighttpd.user
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

# Control the video recorder
recording(){
  case "$1" in
  on)
    /system/sdcard/controlscripts/recording start
    ;;
  off)
    /system/sdcard/controlscripts/recording stop
    ;;
  status)
    if /system/sdcard/controlscripts/recording status | grep -q "PID"
    then
        echo "ON"
    else
        echo "OFF"
    fi
    ;;
  esac
}

# Control the ftp server
ftp_server(){
  case "$1" in
  on)
    /system/sdcard/controlscripts/ftp_server start
    ;;
  off)
    /system/sdcard/controlscripts/ftp_server stop
    ;;
  status)
    if /system/sdcard/controlscripts/ftp_server status | grep -q "PID"
    then
        echo "ON"
    else
        echo "OFF"
    fi
    ;;
  esac
}

# Control the timelapse
timelapse(){
  case "$1" in
  on)
    /system/sdcard/controlscripts/timelapse start
    ;;
  off)
    /system/sdcard/controlscripts/timelapse stop
    ;;
  status)
    if /system/sdcard/controlscripts/timelapse status | grep -q "PID"
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
    /system/sdcard/bin/setconf -k m -v $(get_config /system/sdcard/config/motion.conf motion_sensitivity)
    rewrite_config /system/sdcard/config/motion.conf motion_detection "on"
    ;;
  off)
    /system/sdcard/bin/setconf -k m -v -1
    rewrite_config /system/sdcard/config/motion.conf motion_detection "off"
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

# Control the motion detection mail function
motion_send_mail(){
  case "$1" in
  on)
    rewrite_config /system/sdcard/config/motion.conf send_email "true"
    ;;
  off)
    rewrite_config /system/sdcard/config/motion.conf send_email "false"
    ;;
  status)
    status=$(awk '/send_email/' /system/sdcard/config/motion.conf |cut -f2 -d \=)
    case $status in
      false)
        echo "OFF"
        ;;
      true)
        echo "ON"
        ;;
    esac
  esac
}

# Control the motion detection Telegram function
motion_send_telegram(){
  case "$1" in
  on)
    rewrite_config /system/sdcard/config/motion.conf send_telegram "true"
    ;;
  off)
    rewrite_config /system/sdcard/config/motion.conf send_telegram "false"
    ;;
  status)
    status=$(awk '/send_telegram/' /system/sdcard/config/motion.conf |cut -f2 -d \=)
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
    /system/sdcard/bin/setconf -k n -v 1
    . /system/sdcard/config/autonight.conf
    if [ -z "$ir_led_off" ] || [ $ir_led_off = false ]; then
        ir_led on
    else
        ir_led off
    fi
    ir_cut off
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

# Take a snapshot
snapshot(){
    filename="/tmp/snapshot.jpg"
    /system/sdcard/bin/getimage > "$filename" &
    sleep 1
}

# Update axis
update_axis(){
  . /system/sdcard/config/osd.conf > /dev/null 2>/dev/null
  AXIS=$(/system/sdcard/bin/motor -d s | sed '3d' | awk '{printf ("%s ",$0)}' | awk '{print " X="$2,"Y="$4}')

  if [ "$ENABLE_OSD" = "true" ]; then
    if [ "$DISPLAY_AXIS" = "true" ]; then
      OSD="${OSD}${AXIS}"
    fi

    /system/sdcard/bin/setconf -k o -v "$OSD"
  fi
}

# Set timezone from the timezone config file to system timezone
set_timezone(){
  timezone_name=$(cat /system/sdcard/config/timezone.conf)
  timezone=$(/system/sdcard/bin/busybox awk -F '\t' -v tzn="$timezone_name" '($1==tzn) {print $2}' /system/sdcard/www/timezones.tsv)
  if [ "$(cat /etc/TZ)" != "$timezone" ]; then
    echo "$timezone" > /etc/TZ
  fi
}

# Reboot the System
reboot_system() {
  /sbin/reboot
}

# Re-Mount the SD Card
remount_sdcard() {
  mount -o remount,rw /system/sdcard
}
