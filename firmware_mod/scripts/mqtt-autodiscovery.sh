  #!/bin/sh

  . /system/sdcard/config/mqtt.conf
  . /system/sdcard/scripts/common_functions.sh

  if [ -f /sys/class/net/wlan0/address ]; then
   MAC=$(cat /sys/class/net/wlan0/address)
   MAC_SIMPLE=$(cat /sys/class/net/wlan0/address | tr -d :)
  elif [ -f /sys/class/net/eth0/address ]; then
   MAC=$(cat /sys/class/net/eth0/address)
   MAC_SIMPLE=$(cat /sys/class/net/eth0/address | tr -d :)
  else
   MAC="Unknown"
   MAC_SIMPLE="Unknown"
  fi
  MANUFACTURER="Xiaomi"
  MODEL="Dafang"
  JQ="/system/sdcard/bin/jq -r"
  if [ -s "/system/sdcard/VERSION" ]; then
   V_DATE=$(${JQ} .date /system/sdcard/VERSION)
   V_BRANCH=$(${JQ} .branch /system/sdcard/VERSION)
   V_COMMIT=$(${JQ} .commit /system/sdcard/VERSION)
   VER="${V_DATE} - ${V_BRANCH} - ${V_COMMIT}"
  else
   VER="Need upgrade to have VERSION file"
  fi
  MQTT_COMMAND="/system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t"
  DEVICE_INFO="\"device\": {\"identifiers\": \"$MAC_SIMPLE\", \"connections\": [[\"mac\", \"$MAC\"]], \"manufacturer\": \"$MANUFACTURER\", \"model\": \"$MODEL\", \"name\": \"$DEVICE_NAME\", \"sw_version\": \"$VER\"}"

  # Motion sensor
  $MQTT_COMMAND "$AUTODISCOVERY_PREFIX/binary_sensor/$DEVICE_NAME/motion/config" ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -r -m "{\"name\": \"$DEVICE_NAME motion sensor\", \"unique_id\": \"$MAC_SIMPLE-motion-sensor\", $DEVICE_INFO, \"state_topic\": \"$TOPIC/motion\", \"device_class\": \"motion\"}"

  # Motion detection on/off switch
  $MQTT_COMMAND "$AUTODISCOVERY_PREFIX/switch/$DEVICE_NAME/motion_detection/config" ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -r -m "{\"name\": \"$DEVICE_NAME motion detection\", \"unique_id\": \"$MAC_SIMPLE-motion-detection\", $DEVICE_INFO, \"icon\": \"mdi:motion-sensor\", \"state_topic\": \"$TOPIC/motion/detection\", \"command_topic\": \"$TOPIC/motion/detection/set\"}"

  # Motion send mail alert on/off switch
  $MQTT_COMMAND "$AUTODISCOVERY_PREFIX/switch/$DEVICE_NAME/motion_send_mail/config" ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -r -m "{\"name\": \"$DEVICE_NAME motion send mail\", \"unique_id\": \"$MAC_SIMPLE-motion-send-mail\", $DEVICE_INFO, \"icon\": \"mdi:email-send\", \"state_topic\": \"$TOPIC/motion/send_mail\", \"command_topic\": \"$TOPIC/motion/send_mail/set\"}"

  # Motion send telegram alert on/off switch
  $MQTT_COMMAND "$AUTODISCOVERY_PREFIX/switch/$DEVICE_NAME/motion_send_telegram/config" ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -r -m "{\"name\": \"$DEVICE_NAME motion send telegram\", \"unique_id\": \"$MAC_SIMPLE-motion-send-telegram\", $DEVICE_INFO, \"icon\": \"mdi:telegram\", \"state_topic\": \"$TOPIC/motion/send_telegram\", \"command_topic\": \"$TOPIC/motion/send_telegram/set\"}"

  # Motion detection snapshots
  $MQTT_COMMAND "$AUTODISCOVERY_PREFIX/camera/$DEVICE_NAME/motion_snapshot/config" ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -r -m "{\"name\": \"$DEVICE_NAME motion snapshot\", \"unique_id\": \"$MAC_SIMPLE-motion-snapshot\", $DEVICE_INFO,\"topic\": \"$TOPIC/motion/snapshot/image\"}"

  # Motion tracking on/off switch
  $MQTT_COMMAND "$AUTODISCOVERY_PREFIX/switch/$DEVICE_NAME/motion_tracking/config" ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -r -m "{\"name\": \"$DEVICE_NAME motion tracking\", \"unique_id\": \"$MAC_SIMPLE-motion-tracking\", $DEVICE_INFO, \"icon\": \"mdi:track-light\", \"state_topic\": \"$TOPIC/motion/tracking\", \"command_topic\": \"$TOPIC/motion/tracking/set\"}"

  # LEDs
  $MQTT_COMMAND "$AUTODISCOVERY_PREFIX/switch/$DEVICE_NAME/blue_led/config" ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -r -m "{\"name\": \"$DEVICE_NAME blue led\", \"unique_id\": \"$MAC_SIMPLE-blue-led\", $DEVICE_INFO, \"icon\": \"mdi:led-on\", \"state_topic\": \"$TOPIC/leds/blue\", \"command_topic\": \"$TOPIC/leds/blue/set\"}"
  $MQTT_COMMAND "$AUTODISCOVERY_PREFIX/switch/$DEVICE_NAME/yellow_led/config" ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -r -m "{\"name\": \"$DEVICE_NAME yellow led\", \"unique_id\": \"$MAC_SIMPLE-yellow-led\", $DEVICE_INFO, \"icon\": \"mdi:led-on\", \"state_topic\": \"$TOPIC/leds/yellow\", \"command_topic\": \"$TOPIC/leds/yellow/set\"}"
  $MQTT_COMMAND "$AUTODISCOVERY_PREFIX/switch/$DEVICE_NAME/ir_led/config" ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -r -m "{\"name\": \"$DEVICE_NAME ir led\", \"unique_id\": \"$MAC_SIMPLE-ir-led\", $DEVICE_INFO, \"icon\": \"mdi:led-on\", \"state_topic\": \"$TOPIC/leds/ir\", \"command_topic\": \"$TOPIC/leds/ir/set\"}"

  # IR Filter
  $MQTT_COMMAND "$AUTODISCOVERY_PREFIX/switch/$DEVICE_NAME/ir_cut/config" ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -r -m "{\"name\": \"$DEVICE_NAME ir filter\", \"unique_id\": \"$MAC_SIMPLE-ir-filter\", $DEVICE_INFO, \"icon\": \"mdi:image-filter-black-white\", \"state_topic\": \"$TOPIC/ir_cut\", \"command_topic\": \"$TOPIC/ir_cut/set\"}"

  # Light Sensor
  if [ "$LIGHT_SENSOR" != "false" ]; then
	$MQTT_COMMAND "$AUTODISCOVERY_PREFIX/sensor/$DEVICE_NAME/light_sensor/config" ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -r -m "{\"name\": \"$DEVICE_NAME light sensor\", \"unique_id\": \"$MAC_SIMPLE-light-sensor\", $DEVICE_INFO, \"icon\": \"mdi:brightness-5\", \"unit_of_measurement\": \"%\", \"state_topic\": \"$TOPIC/brightness\"}"
  fi

  # Night mode
  $MQTT_COMMAND "$AUTODISCOVERY_PREFIX/switch/$DEVICE_NAME/night_mode/config" ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -r -m "{\"name\": \"$DEVICE_NAME night mode\", \"unique_id\": \"$MAC_SIMPLE-night-mode\", $DEVICE_INFO, \"icon\": \"mdi:weather-night\", \"state_topic\": \"$TOPIC/night_mode\", \"command_topic\": \"$TOPIC/night_mode/set\"}"

  # Night mode automatic
  $MQTT_COMMAND "$AUTODISCOVERY_PREFIX/switch/$DEVICE_NAME/auto_night_mode/config" ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -r -m "{\"name\": \"$DEVICE_NAME night mode auto\", \"unique_id\": \"$MAC_SIMPLE-night-mode-auto\", $DEVICE_INFO, \"icon\": \"mdi:weather-night\", \"state_topic\": \"$TOPIC/night_mode/auto\", \"command_topic\": \"$TOPIC/night_mode/auto/set\"}"

  # RTSP Server
  $MQTT_COMMAND "$AUTODISCOVERY_PREFIX/switch/$DEVICE_NAME/rtsp_server/config" ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -r -m "{\"name\": \"$DEVICE_NAME rtsp server\", \"unique_id\": \"$MAC_SIMPLE-rtsp-server\", $DEVICE_INFO, \"icon\": \"mdi:cctv\", \"state_topic\": \"$TOPIC/rtsp_server\", \"command_topic\": \"$TOPIC/rtsp_server/set\"}"

  # Motor up/down/left/right
  $MQTT_COMMAND "$AUTODISCOVERY_PREFIX/cover/$DEVICE_NAME/motor_up_down/config" ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -r -m "{\"name\": \"$DEVICE_NAME move up/down\", \"unique_id\": \"$MAC_SIMPLE-move-up-down\", $DEVICE_INFO, \"set_position_topic\": \"$TOPIC/motors/vertical/set\", \"position_topic\": \"$TOPIC/motors/vertical\", \"command_topic\": \"$TOPIC/motors/vertical/set\", \"payload_close\": \"down\", \"payload_open\": \"up\", \"optimistic\": \"false\", \"value_template\": \"{{ ((value|int)/($MAX_Y/$STEP))|round }}\", \"set_position_template\": \"{{ ((position|int)*($MAX_Y/$STEP))|round }}\"}"
  $MQTT_COMMAND "$AUTODISCOVERY_PREFIX/cover/$DEVICE_NAME/motor_left_right/config" ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -r -m "{\"name\": \"$DEVICE_NAME move left/right\", \"unique_id\": \"$MAC_SIMPLE-move-left-right\", $DEVICE_INFO, \"set_position_topic\": \"$TOPIC/motors/horizontal/set\", \"position_topic\": \"$TOPIC/motors/horizontal\", \"command_topic\": \"$TOPIC/motors/horizontal/set\", \"payload_close\": \"right\", \"payload_open\": \"left\", \"optimistic\": \"false\", \"value_template\": \"{{ ((value|int)/($MAX_X/$STEP))|round }}\", \"set_position_template\": \"{{ ((position|int)*($MAX_X/$STEP))|round }}\"}"

  # Recording on/off switch
  $MQTT_COMMAND "$AUTODISCOVERY_PREFIX/switch/$DEVICE_NAME/recording/config" ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -r -m "{\"name\": \"$DEVICE_NAME recording\", \"unique_id\": \"$MAC_SIMPLE-recording\", $DEVICE_INFO, \"icon\": \"mdi:video\", \"state_topic\": \"$TOPIC/recording\", \"command_topic\": \"$TOPIC/recording/set\"}"
