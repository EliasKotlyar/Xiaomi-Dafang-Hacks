#!/bin/sh

setgpio(){
GPIOPIN=$1
echo $2 > /sys/class/gpio/gpio$GPIOPIN/value
}


while true
do
	if [ -f /system/sdcard/config/ldr-average ]; then
		source /system/sdcard/config/ldr-average 2>/dev/null
		#read config in every iteration, so we can change the average online
	fi

	if [ -z $AVG ]; then AVG=1; fi
	# if no config availabe, use 1 as average

	dd if=/dev/jz_adc_aux_0 count=20  |  sed -e 's/[^\.]//g' | wc -m >> /var/run/ldr
	# Add new line to file with measurements

	tail -n $AVG /var/run/ldr > /var/run/ldr-temp
	mv /var/run/ldr-temp  /var/run/ldr
	# cut /var/run/ldr to desired number of lines

	LINES=`cat /var/run/ldr | wc -l`
	if [ $LINES -lt $AVG ]; then AVG=$LINES; fi
	# to avoid slow switching when starting up, use the number of lines when there are less than the average
	# this may cause some flickering when starting up

	SUM=`awk '{s+=$1} END {printf "%.0f", s}' /var/run/ldr`
	#AVGMEASUREMENT=$(( $SUM / $AVG )) # when use and SUM=0, return error divide by zero, solution below:
	[[ ! $SUM -eq 0 -o ! $AVG -eq 0 ]] && AVGMEASUREMENT=$(( $SUM / $AVG )) || AVGMEASUREMENT=0 # calculate the average


	if [ $AVGMEASUREMENT -lt 50 ] # Light detected
	
	then
		setgpio 49 1 # IR-LED Off
		setgpio 25 0 # IR-Cut Off (In my opinion the options are vice-versa: for daylight the IR-Cut has to be on)
		setgpio 26 1 # IR-Cut Off 
		/system/sdcard/bin/setconf -k n -v 0
	
	else # nothing in Buffer -> no light
		setgpio 49 0 # IR-LED on
		setgpio 25 1 # IR-Cut on
		setgpio 26 0 # IR-Cut on
		/system/sdcard/bin/setconf -k n -v 1	
	fi
sleep 10
done

