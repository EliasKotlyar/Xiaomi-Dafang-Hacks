#!/bin/sh
export LD_LIBRARY_PATH='/system/sdcard/lib/:/thirdlib:/system/lib'

. /system/sdcard/scripts/common_functions.sh
if [ -f /system/sdcard/config/ldr-average.conf ]; then
   . /system/sdcard/config/ldr-average.conf 2>/dev/null
   echo "AVG=$AVG - DAYHIGHT=$DAYHIGH - DAYLOW=$DAYLOW - NIGHTHIGH=$NIGHTHIGH - NIGHTLOW=$NIGHTLOW - TIME=$TIME"
fi

while true; do
  if [ -f /system/sdcard/config/ldr-average.conf ]; then
    . /system/sdcard/config/ldr-average.conf 2>/dev/null
    #read config in every iteration, so we can change the average online
  fi

  if [ -z "$AVG" ]; then AVG=1; fi
  # if no config availabe, use 1 as average

  /system/sdcard/bin/getimage > /tmp/snap.jpg
  /system/sdcard/bin/convert /tmp/snap.jpg  -resize 1x1 -colorspace hsb txt:-  | grep "hsb(" | cut -d ',' -f 6 | cut -d '.' -f 1 >> /var/run/ldr

#  dd if=/dev/jz_adc_aux_0 count=20  |  sed -e 's/[^\.]//g' | wc -m >> /var/run/ldr
  # Add new line to file with measurements

  tail -n $AVG /var/run/ldr > /var/run/ldr-temp
  mv /var/run/ldr-temp  /var/run/ldr
  # cut /var/run/ldr to desired number of lines

  LINES=$(wc -l < /var/run/ldr)
  if [ "$LINES" -lt "$AVG" ]; then AVG=$LINES; fi
  # to avoid slow switching when starting up, use the number of lines when there are less than the average
  # this may cause some flickering when starting up

  SUM=$(awk '{s+=$1} END {printf "%.0f", s}' /var/run/ldr)
  [[ ! $SUM -eq 0 || ! $AVG -eq 0 ]] && AVGMEASUREMENT=$(($SUM/$AVG)) || AVGMEASUREMENT=0 # calculate the average

  status=$(night_mode status)
  echo "Status=$status AVGMEASUREMENT =$AVGMEASUREMENT" 
  if [ "$status" == "ON" ]; then
#	  if [ "$AVGMEASUREMENT" -gt "$DAYHIGH" ]; then
#	    echo "Night mode ON, measure=$AVGMEASUREMENT gt than $DAYHIGH => night mode off"
#	    night_mode off
	  if [ "$AVGMEASUREMENT" -gt "$NIGHTHIGH" ]; then
	    echo "Night mode ON, measure="$AVGMEASUREMENT" lt than "$NIGHTHIGH" => night mode off"
	    night_mode off
	  fi
  else
	  if [ "$AVGMEASUREMENT" -lt "$DAYLOW" ]; then  
	    echo "Night mode OFF, measure=$AVGMEASUREMENT lt than $DAYLOW => night mode on"
	    night_mode on
#	  elif [ "$AVGMEASUREMENT" -lt "$NIGHTLOW" ]; then  
#	    echo "Night mode OFF, measure=$AVGMEASUREMENT lt than $NIGHTLOW => night mode on"
#	    night_mode on
	  fi
  fi
  sleep "$TIME"
done
