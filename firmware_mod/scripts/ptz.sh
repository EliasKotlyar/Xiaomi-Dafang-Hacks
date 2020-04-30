#!/bin/sh

###########################################################
### Begin common paths and variables
###########################################################
# Log path (blank will skip logging to file)
log="/system/sdcard/log/ptz.log"

# Include common_functions from Dafang-Hacks
# shellcheck disable=SC1091
. /system/sdcard/scripts/common_functions.sh

# Gets the command name without path
cmd=$(basename "$0")

# Path to motor binary
MOTOR=/system/sdcard/bin/motor.bin

# Path to ptz_presets.conf
FILEPRESETS=/system/sdcard/config/ptz_presets.conf
###########################################################
### End common paths and variables
###########################################################

###########################################################
### Begin Functions
###########################################################
# Script usage help
usage(){
    echo "\
$cmd [OPTION...]
-t, --type    Type of move, can be absolute, relative, or preset.
-p, --preset  Preset name (if type is preset).
-x, -X        X axis position if absolute, number of steps if relative.
-y, -Y        Y axis position if absolute, number of steps if relative.
-h, --help    Show this help.
-v, --verbose Show informational messages (default is warning and error).
-d, --debug   Show script / movement debugging info.
    "
    exit 1
}

# Script usage error
error(){
    echo "$cmd: invalid option '$1'";
    echo "Try '$cmd -h' for more information.";
    exit 1;
}

# Logging
logger() {
    # Usage Examples:
    # logger i "this is informational"
    # logger w "this is a warning"
    # logger e "this is an error"
    # logger d "this is debug"

    timestamp=$(date '+%Y-%m-%d-%H:%M:%S')
    msg=""

    case $1 in
        i|I)
            [ -n "$verbose" ] || [ -n "$debug" ] && msg="Info:    $2"
        ;;
        w|W)
            msg="Warning: $2"
        ;;
        e|E)
            msg="Error:   $2"
        ;;
        d|D)
            [ -n "$debug" ] && msg="Debug:   $2"
        ;;
    esac

    if [ -n "$msg" ]; then
        echo "$cmd: $msg"
        if [ -n "$log" ]; then
            echo "$timestamp: $cmd: $msg" >> $log
        fi
    fi
}

handle_pid() {
    PIDFILE="/var/run/PTZpresets.pid"

    # check pidfile
    if [ -e "$PIDFILE" ] && [ -e "/proc/$(cat $PIDFILE)" ]
    then
        # A process exists with our saved PID
        logger w "PTZpresets.sh is already running with PID $PID_SAVED; exiting"
        exit 1
    fi

    # write pidfile
    if ! logger $$ >"$PIDFILE"
    then
        # If we couldn't save the PID to the lockfile...
        logger e "Failed to create PID file for PID $$ in $PIDFILE; exiting"
        exit 1
    fi

    trap 'rm "$PIDFILE"' EXIT
}

# Calculate relative steps for axis
calculate_relative_steps() {
    case $1 in
        x|X)
            current_x_axis=$($MOTOR -d s | grep "$1" | awk '{print $2}')
            relative_x_steps=$(($2 - current_x_axis))
        ;;
        y|Y)
            current_y_axis=$($MOTOR -d s | grep "$1" | awk '{print $2}')
            relative_y_steps=$(($2 - current_y_axis))
        ;;
        *)
            exit 1
        ;;
    esac
}

### Main
handle_pid

while [ -n "$1" ]; do
    case $1 in
        -t|--type)
            type=$2
            shift
        ;;
        -p|--preset)
            preset=$2
            shift
        ;;
        -x|-X)
            target_x_axis=$2
            shift
            [ "$type" = "relative" ] || calculate_relative_steps x "$target_x_axis"
        ;;
        -y|-Y)
            target_y_axis=$2
            shift
            [ "$type" = "relative" ] || calculate_relative_steps y "$target_y_axis"
        ;;
        -h|--help)
            usage
        ;;
        -v|--verbose)
            verbose=true
        ;;
        -d|--debug)
            debug=true
        ;;
        *)
            error "$1"
        ;;
    esac
    shift
done

move_steps() {
    case $1 in
        x|X)
            case $2 in
                [0-9]*)
                    dir="r"
                ;;
                -[0-9]*)
                    dir="l"
                ;;
                *)
                    logger e "-x must be an integer."
                    exit 1
                ;;
            esac
        ;;
        y|Y)
            case $2 in
                [0-9]*)
                    dir="u"
                ;;
                -[0-9]*)
                    dir="d"
                ;;
                *)
                    logger e "-y must be an integer."
                    exit 1
                ;;
            esac
        ;;
        *)
            logger e "move_steps() usage: move_steps axis steps"
            exit 1
        ;;
    esac

    if [ -n "$flipped" ]; then
        # We are flipped, so check direction variable and reverse
        case $dir in
            u) dir=d ;;
            d) dir=u ;;
            r) dir=l ;;
            l) dir=r ;;
        esac
    fi

    # Motor runs 1.3 time as long as the number of steps.
    steps=$(echo "$2" | sed 's/-//')
    run_time=$(awk -v a="$steps" 'BEGIN{printf ("%f",a*1.3/1000)}')

    motor_cmd="$MOTOR -d $dir -s $steps"
    logger d "Motor command: $motor_cmd"
    $motor_cmd > /dev/null 2>&1
    sleep "$run_time"
}

move_absolute() {
    logger i "Type:   Absolute"
    if [ -n "$relative_x_steps" ]; then
        logger d "X Info: Current: $current_x_axis, Target: $target_x_axis, Relative: $relative_x_steps"
        logger i "X Info: $relative_x_steps steps"

        move_steps x "$relative_x_steps"
    fi
    if [ -n "$relative_y_steps" ]; then
        logger d "Y Info: Current: $current_y_axis, Target: $target_y_axis, Relative: $relative_y_steps"
        logger i "Y Info: $relative_y_steps steps"

        move_steps y "$relative_y_steps"
    fi
}

move_relative() {
    [ "$(/system/sdcard/bin/setconf -g f)" -eq 1 ] && flipped=true
    logger i "Type:   Relative"
    if [ -n "$relative_x_steps" ]; then
        relative_x_steps=$target_x_axis

        logger d "X Info: Current: $current_x_axis, Relative: $relative_x_steps"
        logger i "X Info: $relative_x_steps steps"

        move_steps x "$relative_x_steps"
    fi
    if [ -n "$relative_y_steps" ]; then
        relative_y_steps=$target_y_axis

        logger d "Y Info: Current: $current_y_axis, Relative: $relative_y_steps"
        logger i "Y Info: $relative_y_steps steps"

        move_steps y "$relative_y_steps"
    fi
}

move_preset() {
    if [ -n "$preset" ]; then
        target_x_axis=$(/system/sdcard/bin/jq ".presets.$preset.x" "$FILEPRESETS")
        target_y_axis=$(/system/sdcard/bin/jq ".presets.$preset.y" "$FILEPRESETS")
        if [ "$target_x_axis" = 'null' ]; then
            logger e "Preset $preset is not defined"
        else
            calculate_relative_steps x "$target_x_axis"
            calculate_relative_steps y "$target_y_axis"
            logger i "Type:   Preset"
            logger i "Preset: $preset"
            logger d "X Info: Current: $current_x_axis, Target: $target_x_axis, Relative: $relative_x_steps"
            logger i "X Info: $relative_x_steps steps"

            move_steps x "$relative_x_steps"

            logger d "Y Info: Current: $current_y_axis, Target: $target_y_axis, Relative: $relative_y_steps"
            logger i "Y Info: $relative_y_steps steps"

            move_steps y "$relative_y_steps"
        fi
    else
        logger e "You must specify a preset name (using -p or --preset) when using the preset type."
        exit 1
    fi
}

[ -n "$type" ] || usage

case $type in
    a|absolute)
        move_absolute
    ;;
    p|preset)
        move_preset
    ;;
    r|relative)
        move_relative
    ;;
    *)
        logger e "Type must be one of: a|absolute, p|preset, r|relative."
    ;;
esac

# Update OSD_AXIS
update_axis
