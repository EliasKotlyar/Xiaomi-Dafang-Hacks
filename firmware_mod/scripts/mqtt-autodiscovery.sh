#!/bin/sh

source /system/sdcard/config/mqtt.conf
source /system/sdcard/scripts/common_functions.sh

# Motion sensor
/system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -u "$USER" -P "$PASS" -t "$AUTODISCOVERY_PREFIX/binary_sensor/$DEVICE_NAME/motion/config" ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -m "{\"name\": \"$DEVICE_NAME motion sensor\", \"state_topic\": \"$TOPIC/motion\", \"device_class\": \"motion\"}"

# Motion detection
/system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -u "$USER" -P "$PASS" -t "$AUTODISCOVERY_PREFIX/switch/$DEVICE_NAME/motion_detection/config" ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -m "{\"name\": \"$DEVICE_NAME motion detection\", \"state_topic\": \"$TOPIC/motion/detection\", \"command_topic\": \"$TOPIC/motion/detection/set\"}"

# LEDs
/system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -u "$USER" -P "$PASS" -t "$AUTODISCOVERY_PREFIX/switch/$DEVICE_NAME/blue_led/config" ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -m "{\"name\": \"$DEVICE_NAME blue led\", \"state_topic\": \"$TOPIC/leds/blue\", \"command_topic\": \"$TOPIC/leds/blue/set\"}"
/system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -u "$USER" -P "$PASS" -t "$AUTODISCOVERY_PREFIX/switch/$DEVICE_NAME/yellow_led/config" ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -m "{\"name\": \"$DEVICE_NAME yellow led\", \"state_topic\": \"$TOPIC/leds/yellow\", \"command_topic\": \"$TOPIC/leds/yellow/set\"}"
/system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -u "$USER" -P "$PASS" -t "$AUTODISCOVERY_PREFIX/switch/$DEVICE_NAME/ir_led/config" ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -m "{\"name\": \"$DEVICE_NAME ir led\", \"state_topic\": \"$TOPIC/leds/ir\", \"command_topic\": \"$TOPIC/leds/ir/set\"}"

# IR Filter
/system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -u "$USER" -P "$PASS" -t "$AUTODISCOVERY_PREFIX/switch/$DEVICE_NAME/ir_cut/config" ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -m "{\"name\": \"$DEVICE_NAME ir filter\", \"state_topic\": \"$TOPIC/ir_cut\", \"command_topic\": \"$TOPIC/ir_cut/set\"}"

# Light Sensor
/system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -u "$USER" -P "$PASS" -t "$AUTODISCOVERY_PREFIX/sensor/$DEVICE_NAME/ldr/config" ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -m "{\"name\": \"$DEVICE_NAME light sensor\", \"state_topic\": \"$TOPIC/brightness\"}"

# Night mode
/system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -u "$USER" -P "$PASS" -t "$AUTODISCOVERY_PREFIX/switch/$DEVICE_NAME/night_mode/config" ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -m "{\"name\": \"$DEVICE_NAME night mode\", \"state_topic\": \"$TOPIC/night_mode\", \"command_topic\": \"$TOPIC/night_mode/set\"}"

# Auto Night mode
/system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -u "$USER" -P "$PASS" -t "$AUTODISCOVERY_PREFIX/switch/$DEVICE_NAME/auto_night_mode/config" ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -m "{\"name\": \"$DEVICE_NAME auto night mode\", \"state_topic\": \"$TOPIC/auto_night_mode\", \"command_topic\": \"$TOPIC/auto_night_mode/set\"}"

# RTSP Server
/system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -u "$USER" -P "$PASS" -t "$AUTODISCOVERY_PREFIX/switch/$DEVICE_NAME/rtsp_server/config" ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -m "{\"name\": \"$DEVICE_NAME rtsp server\", \"state_topic\": \"$TOPIC/rtsp_server\", \"command_topic\": \"$TOPIC/rtsp_server/set\"}"
