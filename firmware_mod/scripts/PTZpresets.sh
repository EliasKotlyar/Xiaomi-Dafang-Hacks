#!/bin/sh

################################################
# Created by Nero                              #
# neroxps@gmail.com | 2018-5-28 | v0.0.6 Beta  #
################################################

source /system/sdcard/scripts/common_functions.sh

MOTOR=/system/sdcard/bin/motor
pid=$$
echo $pid > /run/PTZ_$pid.pid

# set log
if [[ -z $3 ]]; then
    LOG=false
else
    LOG=true
fi

logger(){
   if $LOG; then
        echo "$(date '+%Y-%m-%d-%H:%M:%S') $1" >> /system/sdcard/log/ptz.log
   fi
}

# exit
exit_shell(){
    rm -f /run/PTZ_$pid.pid
    exit $1
}


# Get axis status
get_steps(){
    val="$($MOTOR -d s | grep $1 | awk '{print $2}')"
    echo $val
}

move(){
	# Differentiate the coordinates and calculate the number
	# of steps to reach the specified coordinates.
	if [[ "$1" = "X" ]];then 
		grep_text="x"
		opt="r|l"
		text="Right|Left"
	else
		grep_text="y"
		opt="u|d"
		text="Up|Down"
	fi
	SRC_STEPS=$(get_steps $grep_text)
	DST_STEPS=$2
    STEPS=$(awk -v a="$DST_STEPS" -v b="$SRC_STEPS" 'BEGIN{printf ("%d",a-b)}')

    # Motor runs 1.3 time as long as the number of steps.
    SLEEP_NUM=$(awk -v a="${STEPS//-/}" 'BEGIN{printf ("%f",a*1.3/1000)}')

    # "+" Right or Up, "-" Left or Down.
    if [[ $STEPS -gt 0 ]]; then
        $MOTOR -d ${opt%|*} -s "${STEPS//-/}" &>/dev/null
        logger "$1 axis: DST:$DST_STEPS SRC:$SRC_STEPS ${text%|*} $STEPS"
    else
        $MOTOR -d ${opt#*|} -s "${STEPS//-/}" &>/dev/null
        logger "$1 axis DST:$DST_STEPS SRC:$SRC_STEPS ${text#*|} $STEPS"
    fi

    # Waiting for the motor to run.
    sleep ${SLEEP_NUM}
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
    logger "Usage: $(basename $0) [axis_X number] [axis_Y number]"
    exit_shell 1
    ;;  
  [0-9]*)
    move X $1
    ;;
esac

case "$2" in
  *[!0-9]*|"")
    logger "Usage: $(basename $0) [axis_X number] [axis_Y number]"
    exit_shell 2
    ;;  
  [0-9]*)
    move Y $2
    ;; 
esac

# Update OSD_AXIS
update_axis
logger "Move end motor coordinates:$AXIS"
exit_shell 0
