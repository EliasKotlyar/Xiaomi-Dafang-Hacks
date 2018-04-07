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

STEPS=100
FILECAMERAPOS=/tmp/cameraposition

motorLeft(){
      /system/sdcard/bin/motor -d l -s ${1}
}

motorRight(){
      /system/sdcard/bin/motor -d r -s ${1}
}

motorUp() {
      /system/sdcard/bin/motor -d u -s ${1}
}

motorDown() {
      /system/sdcard/bin/motor -d d -s ${1}
}

backtoOrigin() {
    # return to origin for both axis

    # Get values in saved config file
    if [ -f ${FILECAMERAPOS} ]; then
	    origin_x_axis=`grep "x_steps:" ${FILECAMERAPOS} | sed "s/x_steps: //"`
	    origin_y_axis=`grep "y_steps:" ${FILECAMERAPOS} | sed "s/y_steps: //"`
    else
	    origin_x_axis=0
        origin_y_axis=0
    fi

    # Get the current position
    x_axis=`/system/sdcard/bin/motor -d s | grep "x_steps:" | sed "s/x_steps: //"`
    y_axis=`/system/sdcard/bin/motor -d s | grep "y_steps:" | sed "s/y_steps: //"`

	#--------------------------- X Position -------------------------------------------
    #Calculate the difference between the origin and the position now
    if [ ${origin_x_axis} -lt ${x_axis} ]
    then
	    diff=$((${origin_x_axis} - ${x_axis}))

	    #This is a substitution trick to take the abs number
	    diff=${diff#-}
	    motorLeft "${diff}"
    else
	    diff=$((${x_axis} - ${origin_x_axis}))

	    #This is a substitution trick to take the abs number
	    diff=${diff#-}
	    motorRight "${diff}"
    fi
    # Let some time for the motor to turn
    sleep 1

	#--------------------------- Y Position -------------------------------------------
    #Calculate the difference between the origin and the position now
    if [ ${origin_y_axis} -lt ${y_axis} ]
    then
        diff=$((${origin_y_axis} - ${y_axis}))

        #This is a substitution trick to take the abs number
        diff=${diff#-}

        motorDown "${diff}"
    else
        diff=$((${y_axis} - ${origin_y_axis}))

        #This is a substitution trick to take the abs number
        diff=${diff#-}

        motorUp "${diff}"
    fi

    # Let some time for the motor to turn
    sleep 1
}

#################### Start ###

# If no argument that's mean the camera need to return to its original position
# the 5th arguments is '&'
if [ $# -ne 5 ]
then
    backtoOrigin
    return 0;
fi

# Now save the "origin" values of the camera
# Save it to tmp as when the camera reboots the camera are set to 0
if [ -f ${FILECAMERAPOS} ]; then
	/system/sdcard/bin/motor -d s > ${FILECAMERAPOS}
fi


UP=0
DOWN=0
LEFT=0
RIGHT=0

# Display the areas ...
echo $1 $2
echo $3 $4


# Sum all the parameters, that gives the number of region detected
# Only 2 are supported
if [ $((${1} + ${2} + ${3} +${4})) -gt 2 ]
then
	echo "No move if more than 3 detected regions"
    return 0
fi

# Basic algorithm to calculate the movement
# Not optimized, if you have ideas to simplify it ...

if  [ "${1}" == "1" ] && [ "${2}" == "1" ]
then
	UP=1

elif [ "${1}" == "1" ] && [ "${3}" == "1" ]
then
	LEFT=1

elif [ "${2}" == "1" ] && [ "${4}" == "1" ]
then
	RIGHT=1

elif [ "${3}" == "1" ] && [ "${4}" == "1" ]
then
	DOWN=1

elif [ "${1}" == "1" ]
then
	UP=1
	LEFT=1

elif [ "${2}" == "1" ]
then
	UP=1
	RIGHT=1

elif [ "${3}" == "1" ]
then
	LEFT=1
	DOWN=1

elif [ "${4}" == "1" ]
then
	RIGHT=1
	DOWN=1
fi

# Some sanity checks
if [ "${UP}" != 0 ] && [ "${DOWN}" != 0 ]
then
	echo "no move: up and down at the same time"
	return 0
fi
if [ "${RIGHT}" != 0 ] && [ "${LEFT}" != 0 ]
then
	echo "no move: right and left at the same time"
	return 0
fi

if [ ${RIGHT} != 0 ]
then
	echo "Right move"
	motorRight ${STEPS}
fi
if [ ${LEFT} != 0 ]
then
	echo "Left move"
	motorLeft ${STEPS}
fi
if [ ${UP} != 0 ]
then
	echo "Up move"
	motorUp ${STEPS}
fi
if [ ${DOWN} != 0 ]
then
	echo "Down move"
	motorDown ${STEPS}
fi
