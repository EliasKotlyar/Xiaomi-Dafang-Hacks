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
    echo "theme#:#"
    echo "ntp#:#$(cat /system/sdcard/config/ntp_srv.conf)"
    echo "timezone#:#$(/system/sdcard/bin/busybox awk -F '\t' -v tzn="$(cat /system/sdcard/config/timezone.conf)" '{print "<option value=\""$1"\""; if ($1==tzn) print "selected"; print ">" $1 "</option>"}' /system/sdcard/www/json/timezones.tsv | tr -d '\n')"
    echo "currenttime#:#Current time is $(date) - $(cat /etc/TZ)"
  ;;
  save_config)
	if [ -n ${F_hostname} ]; then
		hst=$(printf '%b' "${F_hostname//%/\\x}")
		if [ "$(cat /system/sdcard/config/hostname.conf)" != "$hst" ]; then
	  		echo -n "<p>Setting hostname to '$hst' "
	  		echo "$hst" > /system/sdcard/config/hostname.conf
	  		if hostname "$hst"; then
				echo "Success</p>"
	  		else 
				echo "Failed</p>"
	  		fi
		fi
	fi
	if [ -n ${F_password} ]; then
		password=$(printf '%b' "${F_password//%/\\x}")
		echo "<p>Setting http password to : $password</p>"
		http_password "$password"
	fi
	if [ -n ${F_timezone} ]; then
		timezone_name=$(printf '%b' "${F_timezone//%/\\x}")
		if [ "$(cat /system/sdcard/config/timezone.conf)" != "$timezone_name" ]; then
	  		echo "<p>Setting time zone to '$timezone_name'</p>"
	  		echo "$timezone_name" > /system/sdcard/config/timezone.conf
	  		# Set system timezone from timezone name
	  		set_timezone
		fi
	fi
	if [ -n ${F_ntp} ]; then
		ntp=$(printf '%b' "${F_ntp//%/\\x}")
		if [ $ntp != $(cat /system/sdcard/config/ntp_srv.conf) ]; then
	  		echo "<p>Setting NTP Server to ${ntp} "
	  		echo "$ntp" > /system/sdcard/config/ntp_srv.conf
		fi
	fi
	return
	;;
  *)
    echo "Unsupported command '$F_cmd'"
    ;;

  esac
  fi

exit 0

