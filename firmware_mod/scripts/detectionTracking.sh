#!/bin/sh

# Script to calculate the camera movement
# The screen is split as below (0,1,2,3 are the parameters of the script)
#           +--------------------------------------+
#           |                    |                 |
#           |           0        |      1          |
#           |                    |                 |
#           +--------------------------------------+
#           |                    |                 |
#           |          2         |      3          |
#           |                    |                 |
#           +--------------------------------------+

motorLeft(){      
      /system/sdcard/bin/motor -d l -s 100
}      
                  
motorRight(){  
      /system/sdcard/bin/motor -d r -s 100
}      
                  
motorUp() {                                
      /system/sdcard/bin/motor -d u -s 100
}      
                  
motorDown() {                              
      /system/sdcard/bin/motor -d d -s 100
}     

UP="0"
DOWN="0"
LEFT="0"
RIGHT="0"

echo $1 $2 
echo $3 $4


if [ $(($1 + $2 + $3 +$4)) -gt 2 ]
then
	echo "No move more than 3 detection"
        return 0
fi

# Basic algorithm to calculate the movement
# Not optimized, if you have ideas to simplify it ...

if  [ "${1}" == "1" ] && [ "${2}" == "1" ]
then
	UP="1"

elif [ "${1}" == "1" ] && [ "${3}" == "1" ]  
then
	LEFT="1"


elif [ "${2}" == "1" ] && [ "${4}" == "1" ] 
then
	RIGHT="1"

elif [ "${3}" == "1" ] && [ "${4}" == "1" ] 
then
	DOWN="1"

elif [ "${1}" == "1" ] 
then
	UP="1"
	LEFT="1"

elif [ "${2}" == "1" ] 
then
	UP="1"
	RIGHT="1"

elif [ "${3}" == "1" ] 
then
	LEFT="1"
	DOWN="1"

elif [ "${4}" == "1" ] 
then
	RIGHT="1"
	DOWN="1"
fi


if [ "${UP}" != "0" ] && [ "${DOWN}" != "0" ]
then
	echo "no move: up and down at the same time"
	return 0
fi
if [ "${RIGHT}" != "0" ] && [ "${LEFT}" != "0" ]
then
	echo "no move: right and left at the same time"
	return 0
fi
 
if [ ${RIGHT} != "0" ]
then
	echo "RIGHT"
	motorRight
fi
if [ ${LEFT} != "0" ]
then
	echo "LEFT"
	motorLeft
fi
if [ ${UP} != "0" ]
then
	echo "up"
	motorUp
fi
if [ ${DOWN} != "0" ]
then
	echo "down"
	motorDown
fi

