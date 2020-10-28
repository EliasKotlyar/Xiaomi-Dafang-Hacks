#!/bin/sh                                                          
source ./func.cgi
source /system/sdcard/scripts/common_functions.sh


echo "Content-type: text"
echo "Pragma: no-cache"
echo "Cache-Control: max-age=0, no-store, no-cache"
echo ""

if [ -n "$F_cmd" ]; then
  case "$F_cmd" in
  events)
    echo "["
    find /system/sdcard/DCIM/${F_dir}/ -type f | xargs ls --full-time \
      | awk '{sub(/\/system\/sdcard\/DCIM/, "viewer"); printf "{\"file\" : \"%s\", \"date\" : \"%s %s\"},", $9, $6, $7}' \
      | head -c -1
    echo "]"    
    ;;
  check_sdcard)
	  mount|grep "/system/sdcard"|grep "rw,">/dev/null
	  if [ $? == 1 ]; then
		  echo -n "nok"
	  else
		  echo -n "ok"
	  fi
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
  sdcardInfo)
      echo "sdcardSize#:#$(df -h /system/sdcard | awk 'NR==2{print$4}')"
      echo "sdcardUsed#:#$(df -h /system/sdcard | awk 'NR==2{print$3}')"
      echo "sdcardUsedPercent#:#$(df -h /system/sdcard | awk 'NR==2{print$5}')"
    ;;
  del_file)
    F_file=$(echo ${F_file} | sed -e 's/%2F/\//g' | sed -e 's/viewer/system\/sdcard\/DCIM/') 
    echo "Remove ${F_file}"
    rm $F_file
    ;;
  *)
    echo "Unsupported command '$F_cmd'"
    ;;

  esac
  fi