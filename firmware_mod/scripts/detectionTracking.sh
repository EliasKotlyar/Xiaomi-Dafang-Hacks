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
SLEEP_NUM=0.5

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
if [ $# -eq 0 ]; then
    backtoOrigin
    return 0
fi

# Display the areas ...
echo $1 $2
echo $3 $4

# Sum all the parameters, that gives the number of region detected
# Only 2 are supported
if [ $((${1} + ${2} + ${3} +${4})) -gt 2 ]; then
    echo "no move: more than 2 detected regions"
    return 0
fi

UP=0
DOWN=0
RIGHT=0
LEFT=0

# Calculate the movement
if  [ "${1}" == "1" ] || [ "${2}" == "1" ]; then
    UP=1
fi

if [ "${3}" == "1" ] || [ "${4}" == "1" ]; then
    DOWN=1
fi

if [ "${2}" == "1" ] || [ "${4}" == "1" ]; then
    RIGHT=1
fi

if [ "${1}" == "1" ] || [ "${3}" == "1" ]; then
    LEFT=1
fi

# Sanity checks
if [ ${UP} != 0 ] && [ ${DOWN} != 0 ]; then
    echo "no move vertically: up and down at the same time"
    UP=0
    DOWN=0
fi

if [ ${RIGHT} != 0 ] && [ ${LEFT} != 0 ]; then
    echo "no move horizontally: right and left at the same time"
    RIGHT=0
    LEFT=0
fi

# Do the actual movement
if [ ${UP}    == 1 ]; then
    echo "Move up $STEPS"
    /system/sdcard/bin/motor -d u -s ${STEPS} &>/dev/null
    sleep ${SLEEP_NUM}
fi

if [ ${DOWN}  == 1 ]; then
    echo "Move down $STEPS"
    /system/sdcard/bin/motor -d d -s ${STEPS} &>/dev/null
    sleep ${SLEEP_NUM}
fi

if [ ${RIGHT} == 1 ]; then
    echo "Move right $STEPS"
    /system/sdcard/bin/motor -d r -s ${STEPS} &>/dev/null
    sleep ${SLEEP_NUM}
fi

if [ ${LEFT}  == 1 ]; then
    echo "Move left $STEPS"
    /system/sdcard/bin/motor -d l -s ${STEPS} &>/dev/null
    sleep ${SLEEP_NUM}
fi
