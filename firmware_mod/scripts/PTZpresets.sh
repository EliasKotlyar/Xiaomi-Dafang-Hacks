#!/bin/sh

################################################
# Created by Nero                              #
# neroxps@gmail.com | 2018-5-15 | v0.0.3 Beta  #
################################################

MOTOR=/system/sdcard/bin/motor
pid=$$
echo $pid > /run/PTZ_$pid.pid

# set log
if [[ -z $3 ]]; then
    LOG=false
else
    LOG=ture
fi

loger(){
    if $LOG; then
        echo $1 
    fi
}

exit_shell(){
    rm -f /run/PTZ_$pid.pid
    exit $1
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
      return 1
    elif [[ $2 -gt 800 -o $2 -lt 0 ]]; then
      loger "Y should be between [0-800]"
      return 1
    fi
    return 0
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

# If the previous instruction did not complete, wait for it to complete before continuing.
whit_pid=$(cat /run/PTZ* 2>/dev/null | awk -v pid=$pid '$1<pid{print $1}')
while [[ "$whit_pid" != "" ]] ;do
	whit_pid=$(cat /run/PTZ* 2>/dev/null | awk -v pid=$pid '$1<pid{print $1}')
    sleep 1
done

# Main
case "$1" in
  *[!0-9]*|"")
    loger "Usage: $(basename $0) [axis_X number] [axis_Y number]"
    exit_shell 1
    ;;  
  [0-9]*)
    if ! check_value $1 $2; then
        exit_shell 1
    fi
    move X $1
    ;;
esac

case "$2" in
  *[!0-9]*|"")
    loger "Usage: $(basename $0) [axis_X number] [axis_Y number]"
    exit_shell 2
    ;;  
  [0-9]*)
    move Y $2
    ;; 
esac

# Update OSD_AXIS
source /system/sdcard/config/osd.conf
AXIS="`/system/sdcard/bin/motor -d u -s 0 | tail +5 | awk '{printf (\"%s \",$0)}' |  awk '{print \"X=\"$2,\"Y=\"$4}'`"
/system/sdcard/bin/setconf -k o -v "$OSD"
exit_shell 0