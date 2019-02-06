#!/bin/sh

# Script to calculate the camera movement
# The screen is split as shown below
# (1,2,3,4 are the arguments of the script)
#
#           +--------------------------------------+
#           |                    |                 |
#           |          1         |      2          |
#           |                    |                 |
#           +--------------------------------------+
#           |                    |                 |
#           |          3         |      4          |
#           |                    |                 |
#           +--------------------------------------+

. /system/sdcard/scripts/common_functions.sh

STEPS=$STEP
FILECAMERAPOS=/system/sdcard/config/cameraposition
SLEEP_NUM=$(awk -v a="${STEPS//-/}" 'BEGIN{printf ("%f",a*1.3/1000)}')

backtoOrigin() {

    if [ -f ${FILECAMERAPOS} ]; then
        # Get values in saved config file
        origin_x_axis=`grep "x:" ${FILECAMERAPOS} | sed "s/x: //"`
        origin_y_axis=`grep "y:" ${FILECAMERAPOS} | sed "s/y: //"`
    else
        # No such file exists: create it with the current values
        /system/sdcard/bin/motor -d s > ${FILECAMERAPOS}
    fi

    # return to origin for both axis
    /system/sdcard/scripts/PTZpresets.sh $origin_x_axis $origin_y_axis
}

#################### Start ###

# If no argument that's mean the camera need to return to its original position
if [ $# -eq 0 ]
then
    backtoOrigin
    return 0
fi

# Display the areas ...
echo $1 $2
echo $3 $4

# Sum all the parameters, that gives the number of region detected
# Only 2 are supported
if [ $((${1} + ${2} + ${3} +${4})) -gt 2 ]
then
    echo "No move: more than 3 detected regions"
    return 0
fi

# Diagonals are the only case where we have 2 opposing directions
# (after having ruled out 3 regions or more)
if [ [ "${1}" == "1" ] && [ "${4}" == "1" ] ] || \
   [ [ "${2}" == "1" ] && [ "${3}" == "1" ] ]
then
    echo "No move: diagonally opposed regions"
    return 0
fi

# Basic algorithm to calculate the movement

if  [ "${1}" == "1" ] || [ "${2}" == "1" ]
then
    echo "Move up"
    /system/sdcard/bin/motor -d u -s ${STEPS} &
fi	

if [ "${1}" == "1" ] || [ "${3}" == "1" ]
then
    echo "Move left"
    /system/sdcard/bin/motor -d l -s ${STEPS} &
fi

if [ "${2}" == "1" ] || [ "${4}" == "1" ]
then
    echo "Move right"
    /system/sdcard/bin/motor -d r -s ${STEPS} &
fi

if [ "${3}" == "1" ] || [ "${4}" == "1" ]
then
    echo "Move down"
    /system/sdcard/bin/motor -d d -s ${STEPS} &
fi

# Waiting for the motor to run.
sleep ${SLEEP_NUM}
