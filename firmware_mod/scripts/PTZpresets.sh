#!/bin/sh

################################################
# Created by Nero                              #
# neroxps@gmail.com | 2018-5-15 | v0.0.1 Beta  #
################################################

if [[ -z $3 ]]; then
    LOG=false
else
    LOG=ture
fi

MOTOR=/system/sdcard/bin/motor

loger(){
    if $LOG; then
        echo $1 
    fi
}


# Get axis status
get_steps(){
    val="$($MOTOR -d u -s 0 | grep $1 | awk '{print $2}')"
    echo $val
}

# X should be between [0-2500] and Y should be between [0-800]
check_value(){
    if [[ $1 -gt 2500 -o $1 -lt 0 ]]; then
      loger "X should be between [0-2500]"
      exit 1
    elif [[ $2 -gt 800 -o $2 -lt 0 ]]; then
      loger "Y should be between [0-800]"
      exit 2
    fi
}

move(){
	# Differentiate the coordinates and calculate the number
	# of steps to reach the specified coordinates.
	if [[ "$1" = "X" ]];then 
		grep_text="x_steps"
		opt="r|l"
		text="Right|Left"
	else
		grep_text="y_steps"
		opt="u|d"
		text="Up|Down"
	fi
	SRC_STEPS=$(get_steps $grep_text)
	DST_STEPS=$2
    STEPS=$(awk -v a="$DST_STEPS" -v b="$SRC_STEPS" 'BEGIN{printf ("%d",a-b)}')

    # Motor runs 1.3 time as long as the number of steps.
    SLEEP_NUM=$(awk -v a="$STEPS" 'BEGIN{printf ("%f",a*1.3/1000)}')

    # "+" Right or Up, "-" Left or Down.
    if [[ $STEPS -gt 0 ]]; then
        $MOTOR -d ${opt%|*} -s "${STEPS//-/}" &>/dev/null
        loger "$1 axis: DST:$DST_STEPS SRC:$SRC_STEPS ${text%|*} $STEPS"
    else
        $MOTOR -d ${opt#*|} -s "${STEPS//-/}" &>/dev/null
        loger "$1 axis DST:$DST_STEPS SRC:$SRC_STEPS ${text#*|} $STEPS"
    fi

    # Waiting for the motor to run.
    sleep ${SLEEP_NUM//-/}
}

case "$1" in
  *[!0-9]*|"")
    loger "Usage: $(basename $0) [axis_X number] [axis_Y number]"
    exit 1
    ;;  
  [0-9]*)
    check_value $1 $2
    move X $1
    ;;
esac

case "$2" in
  *[!0-9]*|"")
    loger "Usage: $(basename $0) [axis_X number] [axis_Y number]"
    exit 2
    ;;  
  [0-9]*)
	if [[ $2 -gt 800 -o $2 -lt 0 ]]; then
		loger "Y should be between [0-800]"
		exit 2
	fi
    move Y $2
    ;; 
esac

# Update OSD_AXIS
source /system/sdcard/config/osd.conf
AXIS="`/system/sdcard/bin/motor -d u -s 0 | tail +5 | awk '{printf (\"%s \",$0)}' |  awk '{print \"X=\"$2,\"Y=\"$4}'`"
/system/sdcard/bin/setconf -k o -v "$OSD"