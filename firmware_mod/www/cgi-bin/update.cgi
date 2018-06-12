#!/bin/sh

echo "Content-type: text/html"
echo "Pragma: no-cache"
echo "Cache-Control: max-age=0, no-store, no-cache"
echo ""

cat << EOF
Update:
<pre>`/system/sdcard/autoupdate.sh -v -f -d /system/sdcard/ 2>&1`</pre>
</body>
</html>
EOF
