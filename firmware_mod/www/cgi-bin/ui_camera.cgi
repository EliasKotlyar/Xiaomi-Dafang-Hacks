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
    echo "multicast#:#${MULTICASTDEST}"
	echo "flip#:#${FLIP}"
	echo "codec#:#${CODEC}"
	echo "videoSize#:#${RTSPOPTS}"
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
	if [ -n "${F_codec+x}" ]; then
		video_codec=$(echo "${F_codec}"| sed -e 's/+/ /g')
		rewrite_config /system/sdcard/config/rtspserver.conf CODEC "\"$video_codec\""
		echo "Server video codec set to $video_codec<br/>"
	fi
	if [ -n "${F_videoSize+x}" ]; then
	  	video_size=$(echo "${F_videoSize}"| sed -e 's/+/ /g')
		rewrite_config /system/sdcard/config/rtspserver.conf RTSPOPTS "\"$video_size\""
		echo "Video resolution set to $video_size<br/>"
	fi
	if [ -n "${F_bitRate+x}" ]; then
		brbitrate=$(printf '%b' "${F_bitRate/%/\\x}")
		rewrite_config /system/sdcard/config/rtspserver.conf BITRATE "$brbitrate"
		echo "Bitrate set to $brbitrate<br/>"
	fi
	if [ -n  "${F_format+x}" ]; then
		video_format=$(printf '%b' "${F_format/%/\\x}")
		rewrite_config /system/sdcard/config/rtspserver.conf VIDEOFORMAT "$video_format"
		echo "Video format set to $video_format (0 = FixedQp, 1 = CBR, 2 = VBR and 3 = SMART)<br/>"
	fi
	if [ -n "${F_flip+x}" ]; then
		video_flip=$(echo "${F_flip}"| sed -e 's/+/ /g')
		rewrite_config /system/sdcard/config/rtspserver.conf FLIP "\"$video_flip\""
		echo "Server video flip set to $video_flip<br/>"
	fi
	if [ -n  "${F_frmRateNum+x}" ]; then
		frmRateNum=$(printf '%b' "${F_frmRateNum/%/\\x}")
		if [ "$frmRateNum" != "" ]; then
	  		rewrite_config /system/sdcard/config/rtspserver.conf FRAMERATE_NUM "$frmRateNum"
		fi
	fi
	if [ -n  "${F_frmRateDen+x}" ]; then
		frmRateDen=$(printf '%b' "${F_frmRateDen/%/\\x}")
		if [ "$frmRateDen" != "" ]; then
		  rewrite_config /system/sdcard/config/rtspserver.conf FRAMERATE_DEN "$frmRateDen"
		fi
		echo "FrameRate set to $frmRateDen/$frmRateNum <br/>"
		/system/sdcard/bin/setconf -k d -v "$frmRateNum,$frmRateDen" 2>/dev/null
	fi
	if [ -n  "${F_videoUser+x}" ]; then
		videouser=$(printf '%b' "${F_videoUser//%/\\x}")
		rewrite_config /system/sdcard/config/rtspserver.conf USERNAME "$videouser"

	fi
	if [ -n  "${F_videoPassword+x}" ]; then
		videopassword=$(printf '%b' "${F_videoPassword//%/\\x}")
		rewrite_config /system/sdcard/config/rtspserver.conf USERPASSWORD "$videopassword"
		echo "Set user and password for video stream<br />"
	fi
	if [ -n  "${F_multicast+x}" ]; then
		multicast_dest=$(printf '%b' "${F_multicast//%/\\x}")
		rewrite_config /system/sdcard/config/rtspserver.conf MULTICASTDEST "$multicast_dest"
		echo "Set multicast address to ${multicast_dest}<br />"
	fi
	if [ -n  "${F_videoPort+x}" ]; then
		videoport=$(echo "${F_videoPort}"| tr '\n')
		rewrite_config /system/sdcard/config/rtspserver.conf PORT "$videoport"
		echo "Set video port tp ${videoport}<br />"
	fi
	if [ -n "${F_autoNightMode+x}" ]; then
		rewrite_config /system/sdcard/config/autonight.conf autonight_mode $F_autoNightMode
		echo "Set autonight to mode ${F_autoNightMode} <br />"
	fi
	if [ -n  "${F_avg+x}" ]; then
		ldravg=$(printf '%b' "${F_avg/%/\\x}")
		ldravg=$(echo "$ldravg" | sed "s/[^0-9]//g")
		echo AVG="$ldravg" > /system/sdcard/config/ldr-average.conf
		echo "Average set to $ldravg iterations. <br />"
	fi
	if [ -n  "${F_audioinFormat+x}" ]; then
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
	if [ -n  "${F_audioinBR+x}" ]; then
		audioinBR=$(printf '%b' "${F_audioinBR/%/\\x}")
		if [ "$audioinBR" == "" ]; then
		  audioinBR="8000"
		fi
		rewrite_config /system/sdcard/config/rtspserver.conf AUDIOINBR "$audioinBR"
		echo "In audio bitrate $audioinBR <br/>"
	fi
	if [ -n  "${F_audiooutBR+x}" ]; then
		audiooutBR=$(printf '%b' "${F_audiooutBR/%/\\x}")
		if [ "$audiooutBR" == "" ]; then
			audioOutBR = audioinBR
		fi
		rewrite_config /system/sdcard/config/rtspserver.conf AUDIOOUTBR "$audiooutBR"
		echo "Out audio bitrate $audiooutBR <br/>"
	fi
	if [ -n  "${F_audioinFilter+x}" ]; then
		rewrite_config /system/sdcard/config/rtspserver.conf FILTER "$F_audioinFilter"
		echo "Filter $F_audioinFilter <br/>"
		system/sdcard/bin/setconf -k q -v "$F_audioinFilter" 2>/dev/null
	fi
	if [ -n  "${F_HFEnabled+x}" ]; then
		rewrite_config /system/sdcard/config/rtspserver.conf HIGHPASSFILTER "$F_HFEnabled"
		echo "High Pass Filter $F_HFEnabled <br/>"
		/system/sdcard/bin/setconf -k l -v "$F_HFEnabled" 2>/dev/null
	fi
	if [ -n  "${F_AECEnabled+x}" ]; then
		rewrite_config /system/sdcard/config/rtspserver.conf AECFILTER "$F_AECEnabled"
		echo "AEC Filter $F_AECEnabled <br/>"
		/system/sdcard/bin/setconf -k a -v "$F_AECEnabled" 2>/dev/null
	fi
	if [ -n  "${F_audioinVol+x}" ]; then
		rewrite_config /system/sdcard/config/rtspserver.conf HWVOLUME "$F_audioinVol"
		rewrite_config /system/sdcard/config/rtspserver.conf SWVOLUME "-1"
		echo "Volume $F_audioinVol <br/>"
		/system/sdcard/bin/setconf -k h -v "$F_audioinVol" 2>/dev/null
	fi
	if [ -n  "${F_tlinterval+x}" ]; then
		tlinterval=$(printf '%b' "${F_tlinterval/%/\\x}")
		tlinterval=$(echo "$tlinterval" | sed "s/[^0-9\.]//g")
		if [ "$tlinterval" ]; then
	  		rewrite_config /system/sdcard/config/timelapse.conf TIMELAPSE_INTERVAL "$tlinterval"
	  		echo "Timelapse interval set to $tlinterval seconds. <br />"
		else
	  	echo "Invalid timelapse interval <br />"
		fi
	fi
	if [ -n  "${F_tlduration+x}" ]; then
		tlduration=$(printf '%b' "${F_tlduration/%/\\x}")
		tlduration=$(echo "$tlduration" | sed "s/[^0-9\.]//g")
		if [ "$tlduration" ]; then
	  		rewrite_config /system/sdcard/config/timelapse.conf TIMELAPSE_DURATION "$tlduration"
	  		echo "Timelapse duration set to $tlduration minutes. <br />"
		else
	  		echo "Invalid timelapse duration <br />"
		fi
	fi
	if [ -n  "${F_osdEnable+x}" ]; then
		if [ "${F_osdEnable}" == "true" ]; then
	  		echo "ENABLE_OSD=true" > /system/sdcard/config/osd.conf
	  		update_axis
	  		echo "OSD enabled <br />"
		else
	  		echo "ENABLE_OSD=false" > /system/sdcard/config/osd.conf
	  		echo "OSD disabled <br />"
	  		/system/sdcard/bin/setconf -k o -v ""
		fi
	fi
	if [ -n  "${F_osdText+x}" ]; then
		osdtext=$(printf '%b' "${F_osdText//%/\\x}")
		osdtext=$(echo "$osdtext" | sed -e "s/\\+/ /g")
		echo "OSD=\"${osdtext}\"" | sed -r 's/[ ]X=.*"/"/' >> /system/sdcard/config/osd.conf
		echo "OSD set text ${osdtext}<br />"
	fi
	if [ -n "${F_osdAxis+x}" ];then
		if [ "${F_osdAxis}" == "true" ]; then
			echo "DISPLAY_AXIS=true" >> /system/sdcard/config/osd.conf
			echo "OSD Display axis enabled<br />"
		else
			echo "DISPLAY_AXIS=false" >> /system/sdcard/config/osd.conf
			echo "OSD Display axis disabled<br />"
		fi
	fi
	if [ -n  "${F_osdColor+x}" ]; then
		color='white black red green blue cyan yellow purple'
		echo "COLOR=${F_osdColor}" >> /system/sdcard/config/osd.conf
		/system/sdcard/bin/setconf -k c -v "${F_osdColor}"
		echo -n "Set text color to "
		echo -n $(echo $color | cut -d ' ' -f $(($F_osdColor + 1)))
		echo "<br />"
	fi
	if [ -n  "${F_osdSize+x}" ]; then
		echo "SIZE=${F_osdSize}" >> /system/sdcard/config/osd.conf
		/system/sdcard/bin/setconf -k s -v "${F_osdSize}"
		echo "Set OSD text size to ${F_osdSize}<br />"
	fi
	if [ -n  "${F_osdPixel+x}" ]; then
		echo "SPACE=${F_osdPixel}" >> /system/sdcard/config/osd.conf
		/system/sdcard/bin/setconf -k p -v "${F_osdPixel}"
		echo "Set OSD pixel betwwen chars to ${F_osdPixel}<br />"
	fi
	if [ -n  "${F_osdY+x}" ]; then
		echo "POSY=${F_osdY}" >> /system/sdcard/config/osd.conf
		/system/sdcard/bin/setconf -k x -v "${F_osdY}"
		echo "Set OSD Y position to ${F_osdY}<br />"
	fi
	if [ -n  "${F_osdFixW+x}" ]; then
		echo "FIXEDW=${F_osdFixW}" >> /system/sdcard/config/osd.conf
		/system/sdcard/bin/setconf -k w -v "${F_osdFixW}"
		echo "Set OSD fixed width to ${F_osdFixW}<br />"
	fi
	if [ -n  "${F_osdFonts+x}" ]; then
		fontName=$(printf '%b' "${F_osdFonts//%/\\x}")
		fontName=$(echo "$fontName" | sed -e "s/\\+/ /g")
		echo "FONTNAME=${fontName}" >> /system/sdcard/config/osd.conf
		/system/sdcard/bin/setconf -k e -v "${fontName}"
		echo "Set OSD font to ${fontName}<br />"
	fi
	if [ "$(/system/sdcard/controlscripts/rtsp status)" != "" ]; then
	  echo "Restart rtsp server"
	  /system/sdcard/controlscripts/rtsp stop
	  /system/sdcard/controlscripts/rtsp start
	fi
	return
	;;
  *)
    echo "Unsupported command '$F_cmd'"
    ;;

  esac
  fi

exit 0

