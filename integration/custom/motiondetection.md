## Motion detection scripts

It is possible to run your own scripts on motion detection by adding your executable script (e.g. `.sh`)
to `config/userscripts/motiondetection`

When motion is detected, the first argument to the script will be `on` and when motion detection
ends it will receive `off`.

For example, to send an email containing snapshots on a certain condition, for example 
only when the house is empty, you can check an external service (e.g. openhab)
before triggering the email. 

-- sendEmail.sh --

```$sh
#!/bin/sh

if [ "$1" == "on" ]; then

    source /system/sdcard/config/motion.conf
    source /system/sdcard/scripts/common_functions.sh

    # Check external service to see it anyone present.
    presence=$(/system/sdcard/bin/curl http://openhab/rest/items/PresenceAtHome/state 2>/dev/null)

    if [ "$presence" == "OFF" ] ; then
        # No-one is meant to be here, but motion detected. Send email.
        /system/sdcard/scripts/sendPictureMail.sh &
    fi

fi
```

The files should be copied manually, e.g. using ftp.
