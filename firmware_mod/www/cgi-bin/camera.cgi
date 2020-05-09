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
  	source /system/sdcard/config/rtspserver.conf
	source /system/sdcard/config/autonight.conf
	source /system/sdcard/config/ldr-average.conf
	source /system/sdcard/config/timelapse.conf
	source /system/sdcard/config/osd.conf
    echo "videoSize#:#${RTSPH264OPTS}"
	echo "bitRate#:#${BITRATE}"
	echo "format#:#${VIDEOFORMAT}"
	echo "frmRateNum#:#${FRAMERATE_NUM}"
	echo "frmRateDen#:#${FRAMERATE_DEN}"
	echo "videoUser#:#${USERNAME}"
	echo "videoPassword#:#${USERPASSWORD}"
	echo "videoPort#:#${PORT}"
	echo "autoNightMode#:#${autonight_mode}"
	echo "avg#:#${AVG}"
	echo "audioinFormat#:#${AUDIOFORMAT}"
	echo "audioinBR#:#${AUDIOINBR}"
	echo "audiooutBR#:#${AUDIOOUTBR}"
	echo "audioinFilter#:#$(/system/sdcard/bin/setconf -g q)"
	echo "HFEnabled#:#$(/system/sdcard/bin/setconf -g l)"
	echo "AECEnabled#:#$(/system/sdcard/bin/setconf -g a)"
	echo "audioinVol#:#$(/system/sdcard/bin/setconf -g h)"
	echo "tlinterval#:#${TIMELAPSE_INTERVAL}"
	echo "tlduration#:#${TIMELAPSE_DURATION}"
	echo "osdEnable#:#${ENABLE_OSD}"
	echo "osdText#:#${OSD}"
	echo "osdAxis#:#${DISPLAY_AXIS}"
	echo "osdColor#:#${COLOR}"
	echo "osdSize#:#$(/system/sdcard/bin/setconf -g s)"
	echo "osdPixel#:#${SPACE}"
	echo "osdY#:#${POSY}"
	echo "osdFixW#:#${FIXEDW}"
	echo "osdFonts#:#$(getFonts)"
  ;;
  save_config)
	if [ -n ${F_videoSize} ]; then
	  	video_size=$(echo "${F_videoSize}"| sed -e 's/+/ /g')
		rewrite_config /system/sdcard/config/rtspserver.conf RTSPH264OPTS "\"$video_size\""
		rewrite_config /system/sdcard/config/rtspserver.conf RTSPMJPEGOPTS "\"$video_size\""
		echo "Video resolution set to $video_size<br/>"
	fi
	if [ -n ${F_bitRate} ]; then
		brbitrate=$(printf '%b' "${F_bitRate/%/\\x}")
		rewrite_config /system/sdcard/config/rtspserver.conf BITRATE "$brbitrate"
		echo "Bitrate set to $brbitrate<br/>"
	fi
	if [ -n ${F_format} ]; then
		video_format=$(printf '%b' "${F_format/%/\\x}")
		rewrite_config /system/sdcard/config/rtspserver.conf VIDEOFORMAT "$video_format"
	
	fi
	if [ -n ${F_frmRateNum} ]; then
		frmRateNum=$(printf '%b' "${F_frmRateNum/%/\\x}")
		if [ "$frmRateNum" != "" ]; then
	  		rewrite_config /system/sdcard/config/rtspserver.conf FRAMERATE_NUM "$frmRateNum"
		fi
	fi
	if [ -n ${F_frmRateDen} ]; then
		frmRateDen=$(printf '%b' "${F_frmRateDen/%/\\x}")
		if [ "$frmRateDen" != "" ]; then
		  rewrite_config /system/sdcard/config/rtspserver.conf FRAMERATE_DEN "$frmRateDen"
		fi
		echo "FrameRate set to $frmRateDen/$frmRateNum <br/>"
		/system/sdcard/bin/setconf -k d -v "$frmRateNum,$frmRateDen" 2>/dev/null
	fi

	if [ -n ${F_videoUser} ]; then
		videouser=$(printf '%b' "${F_videoUser//%/\\x}")
		rewrite_config /system/sdcard/config/rtspserver.conf USERNAME "$videouser"
	fi
	if [ -n ${F_videoPassword} ]; then
		videopassword=$(printf '%b' "${F_videoPassword//%/\\x}")
		rewrite_config /system/sdcard/config/rtspserver.conf USERPASSWORD "$videopassword"
	fi
	if [ -n ${F_videoPort} ]; then
		videoport=$(echo "${F_videoPort}"| sed -e 's/+/ /g')
		rewrite_config /system/sdcard/config/rtspserver.conf PORT "$videoport"
	fi
	if [ -n ${F_autoNightMode} ]; then
		if [ -z ${F_autoNightMode} ]; then
			echo "Activate auto night mode"
			/system/sdcard/controlscripts/auto-night-detection start
		else
			echo "Disable auto night mode"
			/system/sdcard/controlscripts/auto-night-detection stop
		fi
	fi
	if [ -n ${F_avg} ]; then
		ldravg=$(printf '%b' "${F_avg/%/\\x}")
		ldravg=$(echo "$ldravg" | sed "s/[^0-9]//g")
		echo AVG="$ldravg" > /system/sdcard/config/ldr-average.conf
		echo "Average set to $ldravg iterations."
	fi
	if [ -n ${F_audioinFormat} ]; then
		audioinFormat=$(printf '%b' "${F_audioinFormat/%/\\x}")
		if [ "$audioinFormat" == "OPUS" ]; then
		  audioOutBR="48000"
		fi
		if [ "$audioinFormat" == "PCM" ]; then
		  audioOutBR = audioinBR
		fi
		if [ "$audioinFormat" == "PCMU" ]; then
			audioOutBR = audioinBR
		fi
		rewrite_config /system/sdcard/config/rtspserver.conf AUDIOFORMAT "$audioinFormat"
		echo "Audio format $audioinFormat <br/>"
	fi
	if [ -n ${F_audioinBR} ]; then
		audioinBR=$(printf '%b' "${F_audioinBR/%/\\x}")
		if [ "$audioinBR" == "" ]; then
		  audioinBR="8000"
		fi
		rewrite_config /system/sdcard/config/rtspserver.conf AUDIOINBR "$audioinBR"
		echo "In audio bitrate $audioinBR <br/>"
	fi
	if [ -n ${F_audiooutBR} ]; then
		audiooutBR=$(printf '%b' "${F_audiooutBR/%/\\x}")
		if [ "$audiooutBR" == "" ]; then
			audioOutBR = audioinBR
		fi
		rewrite_config /system/sdcard/config/rtspserver.conf AUDIOOUTBR "$audiooutBR"
		echo "Out audio bitrate $audiooutBR <br/>"
	fi
	if [ -n ${F_audioinFilter} ]; then
		rewrite_config /system/sdcard/config/rtspserver.conf FILTER "$F_audioinFilter"
		echo "Filter $F_audioinFilter <br/>"
		system/sdcard/bin/setconf -k q -v "$F_audioinFilter" 2>/dev/null
	fi
	if [ -n ${F_HFEnabled} ]; then
		rewrite_config /system/sdcard/config/rtspserver.conf HIGHPASSFILTER "$F_HFEnabled"
		echo "High Pass Filter $F_HFEnabled <br/>"
		/system/sdcard/bin/setconf -k l -v "$F_HFEnabled" 2>/dev/null
	fi
	if [ -n ${F_AECEnabled} ]; then
		rewrite_config /system/sdcard/config/rtspserver.conf AECFILTER "$F_AECEnabled"
		echo "AEC Filter $F_AECEnabled <br/>"
		/system/sdcard/bin/setconf -k a -v "$F_AECEnabled" 2>/dev/null
	fi
	if [ -n ${F_audioinVol} ]; then
		rewrite_config /system/sdcard/config/rtspserver.conf HWVOLUME "$F_audioinVol"
		rewrite_config /system/sdcard/config/rtspserver.conf SWVOLUME "-1"
		echo "Volume $F_audioinVol <br/>"
		/system/sdcard/bin/setconf -k h -v "$F_audioinVol" 2>/dev/null
	fi
	if [ -n ${F_tlinterval} ]; then
		tlinterval=$(printf '%b' "${F_tlinterval/%/\\x}")
		tlinterval=$(echo "$tlinterval" | sed "s/[^0-9\.]//g")
		if [ "$tlinterval" ]; then
	  		rewrite_config /system/sdcard/config/timelapse.conf TIMELAPSE_INTERVAL "$tlinterval"
	  		echo "Timelapse interval set to $tlinterval seconds."
		else
	  	echo "Invalid timelapse interval"
		fi
	fi
	if [ -n ${F_tlduration} ]; then
		tlduration=$(printf '%b' "${F_tlduration/%/\\x}")
		tlduration=$(echo "$tlduration" | sed "s/[^0-9\.]//g")
		if [ "$tlduration" ]; then
	  		rewrite_config /system/sdcard/config/timelapse.conf TIMELAPSE_DURATION "$tlduration"
	  		echo "Timelapse duration set to $tlduration minutes."
		else
	  		echo "Invalid timelapse duration"
		fi
	fi
	if [ -n ${F_osdEnable} ]; then
		enabled=$(printf '%b' "${F_osdEnable}")
		if [ ! -z "$enabled" ]; then
	  		echo "ENABLE_OSD=true" >> /system/sdcard/config/osd.conf
	  		update_axis
	  		echo "OSD enabled"
		else
	  		echo "ENABLE_OSD=false" >> /system/sdcard/config/osd.conf
	  		echo "OSD disabled"
	  		/system/sdcard/bin/setconf -k o -v ""
		fi
	fi
	if [ -n ${F_osdText} ]; then
		osdtext=$(printf '%b' "${F_osdText//%/\\x}")
		osdtext=$(echo "$osdtext" | sed -e "s/\\+/ /g")
		echo "OSD=\"${osdtext}\"" | sed -r 's/[ ]X=.*"/"/' >> /system/sdcard/config/osd.conf
		echo "OSD set<br />"
	fi
	if [ -n ${F_osdAxis} ]; then
		axis_enable=$(printf '%b' "${F_osdAxis}")
		if [ ! -z "$axis_enable" ];then
	  		echo "DISPLAY_AXIS=true" > /system/sdcard/config/osd.conf
	  		echo "DISPLAY_AXIS enable<br />"
		else
	  		echo "DISPLAY_AXIS=false" > /system/sdcard/config/osd.conf
	  		echo "DISPLAY_AXIS disable<br />"
		fi
	fi
	if [ -n ${F_osdColor} ]; then
		echo "COLOR=${F_osdColor}" >> /system/sdcard/config/osd.conf
		/system/sdcard/bin/setconf -k c -v "${F_osdColor}"
	fi
	if [ -n ${F_osdSize} ]; then
		echo "SIZE=${F_osdSize}" >> /system/sdcard/config/osd.conf
		/system/sdcard/bin/setconf -k s -v "${F_osdSize}"
	fi
	if [ -n ${F_osdPixel} ]; then
		echo "SPACE=${F_osdPixel}" >> /system/sdcard/config/osd.conf
		/system/sdcard/bin/setconf -k p -v "${F_osdPixel}"
	fi
	if [ -n ${F_osdY} ]; then
		echo "POSY=${F_osdY}" >> /system/sdcard/config/osd.conf
		system/sdcard/bin/setconf -k x -v "${F_osdY}"
	fi
	if [ -n ${F_osdFixW} ]; then
		echo "FIXEDW=${F_osdFixW}" >> /system/sdcard/config/osd.conf
		/system/sdcard/bin/setconf -k w -v "${F_osdFixW}"
	fi
	if [ -n ${F_osdFonts} ]; then
		fontName=$(printf '%b' "${F_osdFonts//%/\\x}")
		fontName=$(echo "$fontName" | sed -e "s/\\+/ /g")
		echo "FONTNAME=${fontName}" >> /system/sdcard/config/osd.conf
		/system/sdcard/bin/setconf -k e -v "${fontName}"
	fi
	if [ "$(rtsp_h264_server status)" = "ON" ]; then
	  echo "Restart H264 rtsp server"
	  rtsp_h264_server off
	  rtsp_h264_server on
	fi
	if [ "$(rtsp_mjpeg_server status)" = "ON" ]; then
	  echo "Restart MJPEG rtsp server"
	  rtsp_mjpeg_server off
	  rtsp_mjpeg_server on
	fi
	return
	;;
  *)
    echo "Unsupported command '$F_cmd'"
    ;;

  esac
  fi

exit 0

