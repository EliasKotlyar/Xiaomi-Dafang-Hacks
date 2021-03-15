# make our custom binaries visible
PATH=/system/sdcard/bin:$PATH

# overlay new busybox commands over system ones
. ~/.busybox_aliases

# load some convenience functions 
. /system/sdcard/scripts/common_functions.sh

# Add our custom libraries to path
LD_LIBRARY_PATH=/system/sdcard/lib:$LD_LIBRARY_PATH
