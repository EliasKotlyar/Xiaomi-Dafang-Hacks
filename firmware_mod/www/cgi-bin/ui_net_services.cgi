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
  get_config_mqtt)
    if [ ! -f "/system/sdcard/config/mqtt.conf" ]; then
      $(cp /system/sdcard/config/mqtt.conf.dist /system/sdcard/config/mqtt.conf)
    fi
    source /system/sdcard/config/mqtt.conf
    echo "mqttUser#:#${USER}"
    echo "mqttPass#:#${PASS}"
    echo "mqttHost#:#${HOST}"
    echo "mqttPort#:#${PORT}"
    echo "mqttLocation#:#${LOCATION}"
    echo "mqttDeviceName#:#${DEVICE_NAME}"
    echo "mqttAutodiscoveryPrefix#:#${AUTODISCOVERY_PREFIX}"
    echo "mqttStatusInterval#:#${STATUSINTERVAL}"
  ;;
  get_config_mail)
    if [ ! -f "/system/sdcard/config/sendmail.conf" ]; then
      $(cp /system/sdcard/config/sendmail.conf.dist /system/sdcard/config/sendmail.conf)
    fi
    source /system/sdcard/config/sendmail.conf
    echo "from#:#${FROM}"
    echo "fromName#:#${FROMNAME}"
    echo "auth#:#${AUTH}"
    echo "pass#:#${PASS}"
    echo "to#:#${TO}"
    echo "server#:#${SERVER}"
    echo "port#:#${PORT}"
    echo "subject#:#${SUBJECT}"
    echo "body#:#${BODY}"
    echo "numberOfPictures#:#${NUMBEROFPICTURES}"
    echo "timeBetweenSnapshot#:#${TIMEBETWEENSNAPSHOT}"
    echo "quality#:#${QUALITY}"
  ;;
  get_config_telegram)
    if [ ! -f "/system/sdcard/config/telegram.conf" ]; then
      $(cp /system/sdcard/config/telegram.conf.dist /system/sdcard/config/telegram.conf)
    fi
    source /system/sdcard/config/telegram.conf
    echo "apiToken#:#${apiToken}"
    echo "userChatID#:#${userChatId}"
  ;;
  get_config_matrix)
    if [ ! -f "/system/sdcard/config/matrix.conf" ]; then
      $(cp /system/sdcard/config/matrix.conf.dist /system/sdcard/config/matrix.conf)
    fi
    source /system/sdcard/config/matrix.conf
    echo "host#:#${host}"
    echo "portM#:#${port}"
    echo "roomID#:#${room_id}"
    echo "sender#:#${sender}"
    echo "accessToken#:#${access_token}"
	;;
  save_config_mqtt)
    echo "Save mqtt"
    if [ -n "${F_mqttUser+x}" ]; then
      F_mqttUser=$(printf '%b' "${F_mqttUser//%/\\x}")
	    rewrite_config /system/sdcard/config/mqtt.conf USER $F_mqttUser
		  echo "MQTT user set to $F_mqttUser<br/>"
	  fi
    if [ -n "${F_mqttPass+x}" ]; then
      F_mqttPass=$(printf '%b' "${F_mqttPass//%/\\x}")
	    rewrite_config /system/sdcard/config/mqtt.conf PASS $F_mqttPass
		  echo "MQTT password set<br/>"
	  fi
    if [ -n "${F_mqttHost+x}" ]; then
      F_mqttHost=$(printf '%b' "${F_mqttHost//%/\\x}")
	    rewrite_config /system/sdcard/config/mqtt.conf HOST $F_mqttHost
		  echo "MQTT host set to $F_mqttHost<br/>"
	  fi
    if [ -n "${F_mqttPort+x}" ]; then
	    F_mqttPort=$(printf '%b' "${F_mqttPort//%/\\x}")
      rewrite_config /system/sdcard/config/mqtt.conf PORT $F_mqttPort
		  echo "MQTT port set to $F_mqttPort<br/>"
	  fi
    if [ -n "${F_mqttLocation+x}" ]; then
      F_mqttLocation=$(printf '%b' "${F_mqttLocation//%/\\x}")
      rewrite_config /system/sdcard/config/mqtt.conf LOCATION "\"$F_mqttLocation\""
		  echo "MQTT location set to $F_mqttLocation<br/>"
	  fi
    if [ -n "${F_mqttDeviceName+x}" ]; then
	    F_mqttDeviceName=$(printf '%b' "${F_mqttDeviceName//%/\\x}")
      rewrite_config /system/sdcard/config/mqtt.conf DEVICE_NAME "\"$F_mqttDeviceName\""
		  echo "MQTT device name set to $F_mqttDeviceName<br/>"
	  fi
    if [ -n "${F_mqttAutodiscoveryPrefix+x}" ]; then
      F_mqttAutodiscoveryPrefix=$(printf '%b' "${F_mqttAutodiscoveryPrefix//%/\\x}")
      rewrite_config /system/sdcard/config/mqtt.conf AUTODISCOVERY_PREFIX "\"$F_mqttAutodiscoveryPrefix\""
		  echo "MQTT autodiscovery topic set to $F_mqttAutodiscoveryPrefix<br/>"
	  fi
    if [ -n "${F_mqttStatusInterval+x}" ]; then
	    F_mqttStatusInterval=$(printf '%b' "${F_mqttStatusInterval//%/\\x}")
      rewrite_config /system/sdcard/config/mqtt.conf STATUSINTERVAL $F_mqttStatusInterval
		  echo "MQTT status interval set to $F_mqttStatusInterval<br/>"
	  fi
    ;;
  save_config_mail)
    if [ -n "${F_from+x}" ]; then
	    F_from=$(printf '%b' "${F_from//%/\\x}")
      rewrite_config /system/sdcard/config/sendmail.conf FROM "\"$F_from\""
		  echo "Sendmail from address set to $F_from<br/>"
	  fi
    if [ -n "${F_fromName+x}" ]; then
      F_fromName=$(printf '%b' "${F_fromName//%/\\x}")
	    rewrite_config /system/sdcard/config/sendmail.conf FROMNAME "\"$F_fromName\""
		  echo "Sendmail from name set to $F_fromName<br/>"
	  fi
    if [ -n "${F_auth+x}" ]; then
      F_auth=$(printf '%b' "${F_auth//%/\\x}")
	    rewrite_config /system/sdcard/config/sendmail.conf AUTH "\"$F_auth\""
		  echo "Sendmail auth user set to $F_auth<br/>"
	  fi
    if [ -n "${F_pass+x}" ]; then
      F_pass=$(printf '%b' "${F_pass//%/\\x}")
	    rewrite_config /system/sdcard/config/sendmail.conf PASS "\"$F_pass\""
		  echo "Sendmail set password<br/>"
	  fi
    if [ -n "${F_to+x}" ]; then
      F_to=$(printf '%b' "${F_to//%/\\x}")
	    rewrite_config /system/sdcard/config/sendmail.conf TO "\"$F_to\""
		  echo "Sendmail destination address set to $F_to<br/>"
	  fi
    if [ -n "${F_server+x}" ]; then
      F_server=$(printf '%b' "${F_server//%/\\x}")
	    rewrite_config /system/sdcard/config/sendmail.conf SERVER $F_server
		  echo "Sendmail server hostname set to $F_server<br/>"
	  fi
    if [ -n "${F_port+x}" ]; then
      F_port=$(printf '%b' "${F_port//%/\\x}")
	    rewrite_config /system/sdcard/config/sendmail.conf PORT $F_port
		  echo "Sendmail server port set to $F_port<br/>"
	  fi
    if [ -n "${F_subject+x}" ]; then
      F_subject=$(printf '%b' "${F_subject//%/\\x}")
	    rewrite_config /system/sdcard/config/sendmail.conf SUBJECT "\"$F_subject\""
		  echo "Sendmail subject set to $F_subject<br/>"
	  fi
    if [ -n "${F_body+x}" ]; then
      F_body=$(printf '%b' "${F_body//%/\\x}")
	    rewrite_config /system/sdcard/config/sendmail.conf BODY "\"$F_body\""
		  echo "Sendmail body set to $F_body<br/>"
	  fi
    if [ -n "${F_numberOfPictures+x}" ]; then
      F_numberOfPictures=$(printf '%b' "${F_numberOfPictures//%/\\x}")
	    rewrite_config /system/sdcard/config/sendmail.conf NUMBEROFPICTURES $F_numberOfPictures
		  echo "Sendmail number of pictures set to $F_numberOfPictures<br/>"
	  fi
    if [ -n "${F_timeBetweenSnapshot+x}" ]; then
      F_timeBetweenSnapshot=$(printf '%b' "${F_timeBetweenSnapshot//%/\\x}")
	    rewrite_config /system/sdcard/config/sendmail.conf TIMEBETWEENSNAPSHOT $F_timeBetweenSnapshot
		  echo "Sendmail time betweend snapshot set to $F_timeBetweenSnapshot<br/>"
	  fi
    if [ -n "${F_quality+x}" ]; then
      F_quality=$(printf '%b' "${F_quality//%/\\x}")
	    rewrite_config /system/sdcard/config/sendmail.conf QUALITY $F_quality
		  echo "Sendmail quality of pictures set to $F_quality<br/>"
	  fi
    ;;
  save_config_telegram)
    if [ -n "${F_apiToken+x}" ]; then
      F_apiToken=$(printf '%b' "${F_apiToken//%/\\x}")
	    rewrite_config /system/sdcard/config/telegram.conf apiToken "\"$F_apiToken\""
		  echo "Telegram api token set to $F_apiToken<br/>"
	  fi
    if [ -n "${F_userChatID+x}" ]; then
      F_userChatID=$(printf '%b' "${F_userChatID//%/\\x}")
	    rewrite_config /system/sdcard/config/telegram.conf userChatId "\"$F_userChatID\""
		  echo "Matrix server host set to $F_userChatID<br/>"
	  fi
    ;;
  save_config_matrix)
    if [ -n "${F_host+x}" ]; then
      F_host=$(printf '%b' "${F_host//%/\\x}")
	    rewrite_config /system/sdcard/config/matrix.conf host $F_host
		  echo "Matrix server host set to $F_host<br/>"
	  fi
    if [ -n "${F_portM+x}" ]; then
      F_portM=$(printf '%b' "${F_portM//%/\\x}")
	    rewrite_config /system/sdcard/config/matrix.conf port $F_portM
		  echo "Matrix server port set to $F_portM<br/>"
	  fi
      if [ -n "${F_roomID+x}" ]; then
      F_roomID=$(printf '%b' "${F_roomID//%/\\x}")
	    rewrite_config /system/sdcard/config/matrix.conf room_id $F_roomID
		  echo "Matrix room ID set to $F_roomID<br/>"
	  fi
    if [ -n "${F_sender+x}" ]; then
	    F_sender=$(printf '%b' "${F_sender//%/\\x}")
      rewrite_config /system/sdcard/config/matrix.conf sender $F_sender
		  echo "Matrix server sender set to $F_sender<br/>"
	  fi
    if [ -n "${F_accessToken+x}" ]; then
	    F_accessToken=$(printf '%b' "${F_accessToken//%/\\x}")
      rewrite_config /system/sdcard/config/matrix.conf access_token $F_accessToken
		  echo "Matrix server access token set<br/>"
	  fi
    ;;
  *)
    echo "Unsupported command '$F_cmd'"
    ;;

  esac
  fi

exit 0

