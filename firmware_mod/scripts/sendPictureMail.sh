#!/bin/sh

boundary="ZZ_/afg6432dfgkl.94531q"
FILENAME=$(date "+%Y%m%d%H%M%S-")
MAILDATE=$(date -R)

if [ ! -f /system/sdcard/config/sendmail.conf ]; then
  echo "You must configure /system/sdcard/config/sendmail.conf before using sendPictureMail"
  exit 1
fi

. /system/sdcard/config/sendmail.conf

if [ -f /tmp/sendPictureMail.lock ]; then
  echo "sendPictureEmail already running, /tmp/sendPictureMail.lock is present"
  exit 1
fi

touch /tmp/sendPictureMail.lock

export OPENSSL_CONF=/system/sdcard/config/openssl.cnf

# Build headers of the emails
{

printf '%s\n' "From: ${FROMNAME}
To: ${TO}
Subject: ${SUBJECT}
Date: ${MAILDATE}
Mime-Version: 1.0
Content-Type: multipart/mixed; boundary=\"$boundary\"

--${boundary}
Content-Type: text/plain; charset=\"US-ASCII\"
Content-Transfer-Encoding: 7bit
Content-Disposition: inline

${BODY}
"
for i in $(seq 1 ${NUMBEROFPICTURES}); do
	# using sleep and wait so each step takes the specified amount of time
	# instead of the loop-time + the time between snapshots
	if [ ${i} -lt ${NUMBEROFPICTURES} ]; then
		sleep ${TIMEBETWEENSNAPSHOT} &
	fi

	printf '%s\n' "--${boundary}
Content-Type: image/jpeg
Content-Transfer-Encoding: base64
Content-Disposition: attachment; filename=\"${FILENAME}${i}.jpg\"
"

	if [ ${QUALITY} -eq -1 ]; then
		/system/sdcard/bin/getimage | /system/sdcard/bin/openssl enc -base64
	else
	   /system/sdcard/bin/getimage |  /system/sdcard/bin/jpegoptim -m${QUALITY} --stdin --stdout --quiet  | /system/sdcard/bin/openssl enc -base64
	fi

	echo

	# wait for our sleep to finish
	wait
done

# print last boundary with closing --
printf '%s\n' "--${boundary}--"
printf '%s\n' "-- End --"

} | /system/sdcard/bin/busybox sendmail \
-H"exec /system/sdcard/bin/openssl s_client -CAfile /system/sdcard/config/ssl/cacert/cacert.pem -quiet -connect $SERVER:$PORT -starttls smtp" \
-f"$FROM" -au"$AUTH" -ap"$PASS" $TO 2>/dev/null

rm /tmp/sendPictureMail.lock
