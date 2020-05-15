#!/bin/sh
. /system/sdcard/www/cgi-bin/func.cgi
echo "Content-type: text/html"
echo "Pragma: no-cache"
echo "Cache-Control: max-age=0, no-store, no-cache"
echo
if [ "$F_dir" == "recording" ] || [ "$F_dir" == "timelapse" ]; then
echo "<h1 class='is-size-4' >${F_dir} files on SD card</h1>"
cat << EOF
      <table id="files">
        <tr class="header">
            <th>Filename</th>
            <th>Size</th>
            <th>Date</th>
            <th>Actions</th>
        </tr>
EOF
for file in $(find /system/sdcard/DCIM/${F_dir}/ -type f)
        do
         if [[ -f $file ]]; then
          ip_addr=$(ip -o -4 addr show  | sed 's/.* inet \([^/]*\).*/\1/' | grep -v "127.0.0.1")
          file_size=$(ls -lh $file | awk '{print $5}')
          file_url=$(ls -lh $file | awk '{print $9}' | sed 's/\/system\/sdcard\/DCIM/\/viewer/')
          file_date=$(ls -lh $file | awk '{print $6 "-" $7 "-" $8}')
          file_name=$(ls -lh $file | awk '{print $9}' | awk -F / '{print $(NF)}')

          echo "
            <tr>
              <td>${file_name}</td>
              <td>${file_size}</td>
              <td>${file_date}</td>
              <td><a href="${file_url}">download</a>
            </tr>
          "
          fi
        done
echo "</table>"
else
echo "<h1 class='is-size-4' >Wrong parameters</h1>"
fi
