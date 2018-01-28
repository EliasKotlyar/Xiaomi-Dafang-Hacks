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

		else 
	                setgpio 49 0 # IR-LED on
	                setgpio 25 1 # IR-Cut on
	                setgpio 26 0 # IR-Cut on
        fi

	sleep 60
done

