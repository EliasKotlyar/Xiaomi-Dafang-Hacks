#!/bin/sh

boundary="ZZ_/afg6432dfgkl.94531q"
FILENAME=capture.jpg

. /system/sdcard/config/sendmail.conf

# Build headers of the emails
{

printf '%s\n' "From: ${FROMNAME}
To: ${TO}
Subject: ${SUBJECT}
Mime-Version: 1.0
Content-Type: multipart/mixed; boundary=\"$boundary\"

--${boundary}
Content-Type: text/plain; charset=\"US-ASCII\"
Content-Transfer-Encoding: 7bit
Content-Disposition: inline

${BODY}
"
for i in $(seq 1 ${NUMBEROFPICTURES})
do
	# now loop over
	# and produce the corresponding part,
	printf '%s\n' "--${boundary}
Content-Type: image/jpeg
Content-Transfer-Encoding: uuencode
Content-Disposition: attachment; filename=\"${i}${FILENAME}\"
"
        /system/sdcard/bin/getimage | /system/sdcard/bin/busybox uuencode ${i}${FILENAME}

        echo
	if [ ${i} -lt ${NUMBEROFPICTURES} ]
	then
		sleep ${TIMEBETWEENSNAPSHOT}
	fi
done

# print last boundary with closing --
printf '%s\n' "--${boundary}--"

} |  /system/sdcard/bin/busybox sendmail \
-H"exec /system/sdcard/bin/openssl s_client -quiet -connect $SERVER:$PORT -tls1 -starttls smtp" \
-f"$FROM" -au"$AUTH" -ap"$PASS" $TO
