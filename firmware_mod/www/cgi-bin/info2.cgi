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
  get_config)
    echo "hostname#:#$(hostname)"
    echo "model#:#$(detect_model)"
    echo "fwDate#:#$(if [ -s "/system/sdcard/VERSION" ]; then /system/sdcard/bin/jq -r .date /system/sdcard/VERSION; else echo "Never updated. Make an update to get version."; fi)"
    echo "fwBranch#:#$(if [ -s "/system/sdcard/VERSION" ]; then /system/sdcard/bin/jq -r .branch /system/sdcard/VERSION; else echo "Never updated. Make an update to get version."; fi)"
    echo "fwCommit#:#$(if [ -s "/system/sdcard/VERSION" ]; then echo $(check_commit); else echo "Never updated. Make an update to get version."; fi)"
    echo "kernel#:#$(/system/sdcard/bin/busybox uname -v)"
    echo "bootLoader#:#$(busybox strings /dev/mtd0 | grep "U-Boot 2")"
    echo "localTime#:#$(date)"
    echo "uptime#:#$(uptime | sed 's/^.*up *//;s/, *[0-9]* user.*$/m/; s/ day[^0-9]*/d, /;s/ \([hms]\).*m$/\1/;s/:/h, /')"
    echo "loadAvg#:#$(uptime | awk -F': ' '{print $2}')"
	echo "ssid#:#$(/system/bin/iwgetid -r)"
	echo "linkQuality#:#$(cat /proc/net/wireless | awk 'END { print $3 }' | sed 's/\.$//')"
	echo "ip#:#$(ifconfig | grep -E "([0-9]{1,3}\.){3}[0-9]{1,3}" | grep -v 127.0.0.1 | awk '{ print $2 }' | cut -f2 -d:)"
	echo "mac#:#$(cat /sys/class/net/wlan0/address)"
	echo "netmask#:#$(ifconfig wlan0 | sed -rn '2s/ .*:(.*)$/\1/p')"
	echo "gateway#:#$(route | awk '/default/ { print $2}')"
	echo "dns#:#$(cat /etc/resolv.conf | grep nameserver | cut -d ' ' -f 2)"
  	echo "bootMD5#:#$(md5sum /dev/mtd0 |cut -f 1 -d " ")"
	echo "bootVersion#:#$(busybox strings /dev/mtd0 | grep "U-Boot 2")"
	echo "bootCMD#:#$(cat /proc/cmdline)"
	return
 	 ;;
  get_info)
	case "$F_info" in
	netInt)
		ifconfig
		iwconfig
		;;
	netRoutes)
		route
		;;
	netDNS)
		cat /etc/resolv.conf
		;;
	dmesg)
		dmesg
		;;
	logVideo)
		cat /tmp/v4l2rtspserver-master.log
		;;
	logCat)
		/system/bin/logcat -d
		;;
	logUpdate)
		cat /system/sdcard/log/update.log
		;;
	logProcess)
		ps
		;;
	logMounts)
		mount
		;;
	esac
	return
	;;
  *)
    echo "Unsupported command '$F_cmd'"
    ;;

  esac
  fi

exit 0

