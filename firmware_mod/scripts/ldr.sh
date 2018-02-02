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
	if [ -f /system/sdcard/config/rtsp-toggle-night-day ]; then
	# Check if the configuration-option is set

		if [ `cat /sys/class/gpio/gpio49/value` -eq 0 ] && [ `ps w | grep /v4l2rtspserver-master | grep -v grep |  wc -l` -eq 1 ] && [ `ps w | grep /v4l2rtspserver-master | grep -v grep |  grep "\-n" | wc -l` -eq 0 ] ; then
			# if IR LEDs on, v4l2rtspserver running, but without nightvision 
			# switch to b&w
			V4L2RTSPSERVERMASTER=`ps w | grep /v4l2rtspserver-master | grep -v grep | sed -e "s/.*\///"`
			killall v4l2rtspserver-master
			/system/sdcard/bin/busybox nohup /system/sdcard/bin/$V4L2RTSPSERVERMASTER -n &>/dev/null &
		fi

		if [ `cat /sys/class/gpio/gpio49/value` -eq 1 ] && [ `ps w | grep /v4l2rtspserver-master | grep -v grep |  wc -l` -eq 1 ] && [ `ps w | grep /v4l2rtspserver-master | grep -v grep |  grep "\-n" | wc -l` -eq 1 ]; then
			# if IR LEDs off, v4l2rtspserver running, and v4l2rtspserver running with nightvision
			# switch to color
			V4L2RTSPSERVERMASTER=`ps w | grep /v4l2rtspserver-master | grep -v grep | sed -e "s/.*\///" | sed -e "s/\-n//`
			killall v4l2rtspserver-master
			/system/sdcard/bin/busybox nohup /system/sdcard/bin/$V4L2RTSPSERVERMASTER &>/dev/null &
	fi

fi

sleep 30
done

