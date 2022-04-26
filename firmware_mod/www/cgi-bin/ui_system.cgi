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
    echo "github_token#:#$(get_config /system/sdcard/config/updates.conf github_token)"
    echo "wifi_ssid#:#$(wpa_config_get ssid | sed 's/^"\([^"]*\)"$/\1/')"
    echo "connect_timeout#:#$(get_config /system/sdcard/config/wifi.conf connect_timeout)"
    echo "scan_interval#:#$(get_config /system/sdcard/config/wifi.conf scan_interval)"
    echo "ap_ssid#:#$(get_config /system/sdcard/config/hostapd.conf ssid)"
    echo "usb_eth#:#$([ -f /system/sdcard/config/usb_eth_driver.conf ] && echo on || echo off)"
    echo "ssh_key#:#$(cat /system/sdcard/root/.ssh/authorized_keys)"
    echo "ssh_port#:#$(get_config /system/sdcard/config/ssh.conf ssh_port)"
    echo "ssh_password#:#$(get_config /system/sdcard/config/ssh.conf ssh_password)"
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
	if [ -n ${F_github_token+x} ]; then
		github_token=$(printf '%b' "${F_github_token//%/\\x}")
		if [ "$github_token" != "$(get_config /system/sdcard/config/updates.conf github_token)" ]; then
	  		echo "<p>Setting GitHub token</p>"
	  		rewrite_config /system/sdcard/config/updates.conf github_token "$github_token"
		fi
	fi
  if [ -n ${F_wifi_ssid} ]; then
    F_wifi_ssid=$(echo "$F_wifi_ssid" | sed 's/+/ /g')
		wifi_ssid=$(printf '%b' "${F_wifi_ssid//%/\\x}")
		echo "<p>Setting wifi SSID to: $wifi_ssid</p>"
		wpa_config_set ssid "\"$wifi_ssid\""
	fi
  if [ -n ${F_wifi_password} ]; then
		wifi_password=$(printf '%b' "${F_wifi_password//%/\\x}")
		echo "<p>Setting wifi password to: $wifi_password</p>"
		wpa_config_set psk "\"$wifi_password\""
	fi
  if [ -n ${F_ssh_port} ]; then
		ssh_port=$(printf '%b' "${F_ssh_port//%/\\x}")
		echo "<p>Changing SSH port to: $ssh_port</p>"
		rewrite_config /system/sdcard/config/ssh.conf ssh_port "$ssh_port"
	fi
  if [ -n ${F_ssh_password} ]; then
		ssh_password=$(printf '%b' "${F_ssh_password//%/\\x}")
		echo "<p>Changing SSH password to: $ssh_password</p>"
		rewrite_config /system/sdcard/config/ssh.conf ssh_password "$ssh_password"
	fi
  if [ -n ${F_ssh_key} ]; then
		ssh_key=$(printf '%b' "${F_ssh_key//%/\\x}" | sed 's/%20/ /g')
		echo "<p>Changing SSH key to: $ssh_key</p>"
		echo "$ssh_key" > /system/sdcard/root/.ssh/authorized_keys
	fi

  if [ -n ${F_ssh_key} ] || [ -n ${F_ssh_password} ] || [ -n ${F_ssh_port} ]; then
  		echo "Re" 
		/system/sdcard/controlscripts/dropbear stop 
          	/system/sdcard/controlscripts/dropbear start
  fi
  if [ -n ${F_connect_timeout} ]; then
    F_connect_timeout=$(echo "$F_connect_timeout" | sed 's/+/ /g')
    connect_timeout=$(printf '%b' "${F_connect_timeout//%/\\x}")
    echo "<p>Setting wifi connect timeout to: $connect_timeout</p>"
    rewrite_config /system/sdcard/config/wifi.conf connect_timeout "$connect_timeout"
  fi
  if [ -n ${F_scan_interval} ]; then
    F_scan_interval=$(echo "$F_scan_interval" | sed 's/+/ /g')
    scan_interval=$(printf '%b' "${F_scan_interval//%/\\x}")
    echo "<p>Setting access point scan interval to: $scan_interval</p>"
    rewrite_config /system/sdcard/config/wifi.conf scan_interval "$scan_interval"
  fi
  if [ -n ${F_ap_ssid} ]; then
    F_ap_ssid=$(echo "$F_ap_ssid" | sed 's/+/ /g')
    ap_ssid=$(printf '%b' "${F_ap_ssid//%/\\x}")
    echo "<p>Setting access point SSID to: $ap_ssid</p>"
    rewrite_config /system/sdcard/config/hostapd.conf ssid "$ap_ssid"
  fi
  if [ -n ${F_ap_password} ]; then
    ap_password=$(printf '%b' "${F_ap_password//%/\\x}")
    echo "<p>Setting access point password to: $ap_password</p>"
    rewrite_config /system/sdcard/config/hostapd.conf wpa_passphrase "$ap_password"
  fi
  if [ -n ${F_usb_eth} ]; then
    usb_eth=$(printf '%b' "${F_usb_eth//%/\\x}")
    if [ "$usb_eth" = "on" ]; then
      echo "<p>Enabling USB ethernet</p>"
      touch /system/sdcard/config/usb_eth_driver.conf
    else
      echo "<p>Disabling USB ethernet</p>"
      rm -f /system/sdcard/config/usb_eth_driver.conf
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
