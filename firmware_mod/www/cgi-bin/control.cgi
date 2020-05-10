#!/bin/sh

. /system/sdcard/www/cgi-bin/func.cgi
. /system/sdcard/scripts/common_functions.sh

export LD_LIBRARY_PATH=/system/lib
export LD_LIBRARY_PATH=/thirdlib:$LD_LIBRARY_PATH

echo "Content-type: text/html"
echo "Pragma: no-cache"
echo "Cache-Control: max-age=0, no-store, no-cache"
echo ""

if [ -n "$F_cmd" ]; then
  case "$F_cmd" in
  get_services)
	echo "auto_night_mode#:#$(auto_night_mode status)#:#$(test -f /system/sdcard/config/autostart/auto_night_mode && echo 'true' || echo 'false')"
    echo "debug-on-osd#:#$(debug_on_osd status)#:#$(test -f /system/sdcard/config/autostart/debug-on-osd && echo 'true' || echo 'false')"
    echo "ftp_server#:#$(ftp_server status)#:#$(test -f /system/sdcard/config/autostart/ftp_server && echo 'true' || echo 'false')"
    echo "mqtt-control#:#$(mqtt_control status)#:#$(test -f /system/sdcard/config/autostart/mqtt-control && echo 'true' || echo 'false')"
    echo "mqtt-status#:#$(mqtt_status status)#:#$(test -f /system/sdcard/config/autostart/mqtt-status && echo 'true' || echo 'false')"
    echo "onvif-srvd#:#$(onvif_srvd status)#:#$(test -f /system/sdcard/config/autostart/onvif-srvd && echo 'true' || echo 'false')"
    echo "recording#:#$(recording status)#:#$(test -f /system/sdcard/config/autostart/recording && echo 'true' || echo 'false')"
    echo "rtsp-h264#:#$(rtsp_h264_server status)#:#$(test -f /system/sdcard/config/autostart/rtsp-h264 && echo 'true' || echo 'false')"
    echo "rtsp-mjpeg#:#$(rtsp_mjpeg_server status)#:#$(test -f /system/sdcard/config/autostart/rtsp-mjpeg && echo 'true' || echo 'false')"
	echo "sound-on-startup#:#$(sound_on_startup status)#:#$(test -f /system/sdcard/config/autostart/sound-on-startup && echo 'true' || echo 'false')"
	echo "telegram-bot#:#$(telegram_bot status)#:#$(test -f /system/sdcard/config/autostart/telegram-bot && echo 'true' || echo 'false')"
	echo "timelapse#:#$(timelapse status)#:#$(test -f /system/sdcard/config/autostart/timelapse && echo 'true' || echo 'false')"
	return
	;;
  reboot)
  	echo "Rebooting device..."
	/sbin/reboot
	return
	;;
  shutdown)
	echo "Shutting down device.."
	/sbin/halt
	return
	;;
  *)
    echo "Unsupported command '$F_cmd'"
    ;;

  esac
  fi

exit 0

