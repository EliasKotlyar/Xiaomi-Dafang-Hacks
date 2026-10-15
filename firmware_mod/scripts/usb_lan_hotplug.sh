#!/bin/sh
# Kernel hotplug helper for the diagnostic USB LAN interface.
# run.sh writes this path to /proc/sys/kernel/hotplug after Wi-Fi starts, only
# with LAN_MODE=diag in usb_eth.conf. The kernel runs it for every event, so keep it small.
# Every event goes first to /sbin/mdev, the stock helper (see
# hacks/firmware/rcfile.sh), with the same arguments and environment.
# Then, only for a USB LAN interface (eth*):
#   add: net_select.sh diag starts the DHCP client again, in the background.
#   remove: net_select.sh stop stops the old client and removes its routing.
/sbin/mdev "$@"
status=$?

case "$SUBSYSTEM:$ACTION:$INTERFACE" in
  net:add:eth*) mode=diag ;;
  net:remove:eth*) mode=stop ;;
  *) exit "$status" ;;
esac

PATH=/sbin:/usr/sbin:/bin:/usr/bin:/system/bin:/system/sdcard/bin
export PATH
if [ "$mode" = diag ]; then
  /system/sdcard/scripts/net_select.sh diag > /dev/null 2>&1 &
else
  /system/sdcard/scripts/net_select.sh stop "$INTERFACE" > /dev/null 2>&1
fi
exit "$status"
