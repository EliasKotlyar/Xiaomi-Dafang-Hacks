#!/bin/sh

. /system/sdcard/www/cgi-bin/func.cgi

export LD_LIBRARY_PATH=/system/lib
export LD_LIBRARY_PATH=/thirdlib:$LD_LIBRARY_PATH

echo "Content-type: text/html"
echo "Pragma: no-cache"
echo "Cache-Control: max-age=0, no-store, no-cache"
echo ""

if [ -n "$F_cmd" ]; then
  case "$F_cmd" in
  get_services)
    services="auto-night-detection debug-on-osd ftp_server mqtt-control mqtt-status onvif-srvd recording rtsp sound-on-startup telegram-bot timelapse"
    for service in $services ; do  
      echo "${service}#:#$(test -f /run/${service}.pid && echo 'started' || echo 'stopped')#:#$(test -f /system/sdcard/config/autostart/${service} && echo 'true' || echo 'false')#:#false"
    done
	return
	;;
  autoStartService)
    if [ $F_service == "auto_night_mode" ]; then
      F_service="auto-night-detection"
    fi
    if $F_action ; then
      echo "#!/bin/sh" > "/system/sdcard/config/autostart/${F_service}"
      echo "/system/sdcard/controlscripts/${F_service}" >> "/system/sdcard/config/autostart/${F_service}"
    else
      rm "/system/sdcard/config/autostart/${F_service}"
    fi
    return
    ;;
  services)
    $(/system/sdcard/controlscripts/${F_service} $F_action) > /dev/null
    return
    ;;
  getFiles)
    ip_addr=$(ip -o -4 addr show  | sed 's/.* inet \([^/]*\).*/\1/' | grep -v "127.0.0.1")
    for file in $(find /system/sdcard/DCIM/${F_dir}/ -type f)
      do                                                 
        if [[ -f $file ]]; then                           
          file_size=$(ls -lh $file | awk '{print $5}')                                          
          file_url=$(ls -lh $file | awk '{print $9}' | sed 's/\/system\/sdcard\/DCIM/\/viewer/')
          file_date=$(ls -lh $file | awk '{print $6 "-" $7 "-" $8}')                            
          file_name=$(ls -lh $file | awk '{print $9}' | awk -F / '{print $(NF)}')                                                                                                      
          echo "${file_name}#:#${file_size}#:#${file_date}#:#${file_url}"                                                                                    
        fi                                        
      done             
    return
    ;;

  del_config)
    F_file=$(echo ${F_file} | sed -e 's/%2F/\//g' | sed -e 's/viewer/system\/sdcard\/DCIM/') 
    echo "Remove ${F_file}"
    rm $F_file
  ;;
  restore_config)
    F_file=$(echo ${F_file} | sed -e 's/%2F/\//g' | sed -e 's/viewer/system\/sdcard\/DCIM/') 
    tar -xf $F_file -C /system/sdcard/config/
    echo "Restore done"
    /sbin/reboot
  ;;
  save_config)
    /system/sdcard/controlscripts/saveConfig.sh
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

