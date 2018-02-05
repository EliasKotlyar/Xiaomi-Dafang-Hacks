#!/bin/sh

setgpio(){
GPIOPIN=$1
echo $2 > /sys/class/gpio/gpio$GPIOPIN/value
}


while true
do
	if [ `dd if=/dev/jz_adc_aux_0 count=20  |  sed -e 's/[^\.]//g' | wc -m` -lt 50 ]; # Light detected
	
	then
		setgpio 49 1 # IR-LED Off
		setgpio 25 0 # IR-Cut Off (In my opinion the options are vice-versa: for daylight the IR-Cut has to be on)
		setgpio 26 1 # IR-Cut Off 
	
	else # nothing in Buffer -> no light
		setgpio 49 0 # IR-LED on
		setgpio 25 1 # IR-Cut on
		setgpio 26 0 # IR-Cut on
	
	fi

# Toggle nightvision in v4l2rtspserver
	if [ -f /var/run/auto-toggle-nightvision ]; then
	# Check if the configuration-option is set

 # MJPeg
 
                 if [ `cat /sys/class/gpio/gpio49/value` -eq 0 ] && [ -f /var/run/v4l2rtspserver-master-mjpeg.pid ] && [ ! -f /var/run/v4l2rtspserver-master-mjpeg.night ] ; then
                        # if IR LEDs on, v4l2rtspserver-master-mjpeg running, but without nightvision
                        # switch to night-mode
			/system/sdcard/controlscripts/rtsp-mjpeg stop
			/system/sdcard/controlscripts/rtsp-mjpeg startnight                 
	         fi

		if [ `cat /sys/class/gpio/gpio49/value` -eq 1 ]&& [ -f /var/run/v4l2rtspserver-master-mjpeg.night ]  ; then
			# if IR LED off, v4l2rtspserver-master-mjpeg running with nightvision
			/system/sdcard/controlscripts/rtsp-mjpeg stop
			/system/sdcard/controlscripts/rtsp-mjpeg start
		fi

# H264 with segmentation

                 if [ `cat /sys/class/gpio/gpio49/value` -eq 0 ] && [ -f /var/run/v4l2rtspserver-master-h264-s.pid ] && [ ! -f /var/run/v4l2rtspserver-master-h264-s.night ] ; then
                        # if IR LEDs on, v4l2rtspserver-master-h264-s running, but without nightvision
                        # switch to night-mode
                        /system/sdcard/controlscripts/rtsp-h264-with-segmentation stop
                        /system/sdcard/controlscripts/rtsp-h264-with-segmentation startnight
                 fi

                if [ `cat /sys/class/gpio/gpio49/value` -eq 1 ]&& [ -f v4l2rtspserver-master-h264-s.night ]  ; then
                        # if IR LED off, v4l2rtspserver-master-h264-s running with nightvision
                        /system/sdcard/controlscripts/rtsp-h264-with-segmentation stop
                        /system/sdcard/controlscripts/rtsp-h264-with-segmentation start
                fi


# H264

                 if [ `cat /sys/class/gpio/gpio49/value` -eq 0 ] && [ -f /var/run/v4l2rtspserver-master-h264.pid ] && [ ! -f /var/run/v4l2rtspserver-master-h264.night ] ; then
                        # if IR LEDs on, v4l2rtspserver-master-h264 running, but without nightvision
                        # switch to night-mode
                        /system/sdcard/controlscripts/rtsp-h264 stop
                        /system/sdcard/controlscripts/rtsp-h264 startnight
                 fi

                if [ `cat /sys/class/gpio/gpio49/value` -eq 1 ]&& [ -f v4l2rtspserver-master-h264.night ]  ; then
                        # if IR LED off, v4l2rtspserver-master-h264 running with nightvision
                        /system/sdcard/controlscripts/rtsp-h264 stop
                        /system/sdcard/controlscripts/rtsp-h264 start
                fi


fi

sleep 30
done

