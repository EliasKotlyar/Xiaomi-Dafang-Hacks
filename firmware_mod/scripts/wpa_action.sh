#!/bin/sh

WIFI_BIN=/system/sdcard/scripts/wifi.sh

case "$2" in
  CONNECTED)
    "$WIFI_BIN" wpa_action connected
    ;;
  DISCONNECTED)
    "$WIFI_BIN" wpa_action disconnected
    ;;
esac
