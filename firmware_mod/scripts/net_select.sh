#!/bin/sh
# Bring up a supported USB Ethernet adapter (list: LAN_USB_DEVICES, see config/usb_eth.conf.dist).
# "force" (run.sh, with config/usb_eth_driver.conf): the adapter is the main interface.
#   Exit 0 when the adapter has a network interface, do not wait for a link.
#   Exit 1 (no adapter, driver or interface) so run.sh starts Wi-Fi.
# "diag" (run.sh in the background after Wi-Fi starts, only with LAN_MODE=diag in
#   config/usb_eth.conf): the adapter gets a DHCP address for diagnostics, without
#   default route or DNS. Wi-Fi stays the main interface. usb_lan_hotplug.sh runs
#   it again when the adapter is plugged in.
# "stop <interface>" (usb_lan_hotplug.sh, adapter removed): stop the diag client.
MODE="$1"

# ifconfig and udhcpc are only in /sbin. An SSH shell and the kernel hotplug
# helper can have a PATH without /sbin.
PATH=/sbin:/usr/sbin:/bin:/usr/bin:/system/bin:/system/sdcard/bin
export PATH

# Stop the diag DHCP client of interface $1 (boot or earlier hot-plug run), then
# remove its address and routing. udhcpc does not run its script when it stops.
stop_diag_client() {
  local pid i
  pid=$(cat "/var/run/udhcpc.$1.pid" 2>/dev/null)
  if [ -n "$pid" ] && kill "$pid" 2>/dev/null; then
    # Wait until it exits, so that it cannot add its routing again
    i=0
    while kill -0 "$pid" 2>/dev/null && [ "$i" -lt 5 ]; do
      sleep 1
      i=$((i + 1))
    done
  fi
  interface="$1" /system/sdcard/scripts/udhcpc-diag.script deconfig 2>/dev/null
}

if [ "$MODE" = stop ]; then
  stop_diag_client "$2"
  exit 0
fi

# Included for configure_static_net_iface
. /system/sdcard/scripts/common_functions.sh

CONFIGPATH=/system/sdcard/config
DRIVERPATH=/system/sdcard/driver

# Defaults. Override them in config/usb_eth.conf (see usb_eth.conf.dist).
LAN_USB_DEVICES="0b95:772b:usbnet,asix 0b95:7720:usbnet,asix 0b95:772a:usbnet,asix 0b95:1780:usbnet,asix 0bda:8152:r8152"
LAN_ENUM_WAIT=3
LAN_MAC=""
if [ -f "$CONFIGPATH/usb_eth.conf" ]; then
  . "$CONFIGPATH/usb_eth.conf"
fi

USB_DEV=""
USB_MODULES=""
LOADED_MODULES=""
LAN_IFACE=""

# Diag runs at boot and at each hot-plug add. A second run at the same time
# (for example the add event of the interface that the boot run creates) exits.
LOCK=/var/run/net_select.diag.lock
if [ "$MODE" = diag ]; then
  if ! mkdir "$LOCK" 2>/dev/null; then
    echo "USB_ETHERNET: diag is already running"
    exit 0
  fi
  trap 'rmdir "$LOCK"' EXIT
fi

# Set USB_DEV and USB_MODULES for the first configured adapter that is plugged in.
find_usb_adapter() {
  local entry dev id
  for entry in $LAN_USB_DEVICES; do
    for dev in /sys/bus/usb/devices/*; do
      [ -f "$dev/idVendor" ] && [ -f "$dev/idProduct" ] || continue
      id="$(cat "$dev/idVendor"):$(cat "$dev/idProduct")"
      case "$entry" in
        "$id":*)
          USB_DEV="$dev"
          USB_MODULES="${entry#"$id":}"
          return 0
          ;;
      esac
    done
  done
  return 1
}

# Undo what this script did and tell run.sh to start Wi-Fi.
# In force mode, once the interface exists, only report the error.
fail() {
  local module
  if [ "$MODE" = force ] && [ -n "$LAN_IFACE" ]; then
    echo "USB_ETHERNET: $1. Forced, Wi-Fi not started." >&2
    return
  fi
  echo "USB_ETHERNET: $1. Using Wi-Fi." >&2
  if [ -n "$LAN_IFACE" ]; then
    ifconfig "$LAN_IFACE" down
  fi
  for module in $LOADED_MODULES; do
    rmmod "$module"
  done
  exit 1
}

i=0
until find_usb_adapter; do
  i=$((i + 1))
  if [ "$i" -ge "$LAN_ENUM_WAIT" ]; then
    echo "USB_ETHERNET: No configured USB Ethernet adapter found"
    exit 1
  fi
  sleep 1
done
echo "USB_ETHERNET: Found adapter $USB_DEV, modules $USB_MODULES"

for module in $(echo "$USB_MODULES" | tr ',' ' '); do
  # Skip modules that are loaded, and drivers built into the kernel (some kernels have r8152)
  if grep -q "^$module " /proc/modules || [ -d "/sys/bus/usb/drivers/$module" ]; then
    continue
  fi
  if [ ! -f "$DRIVERPATH/$module.ko" ]; then
    fail "Driver $DRIVERPATH/$module.ko is missing"
  fi
  insmod "$DRIVERPATH/$module.ko" || fail "Could not load $module.ko"
  # Keep reverse load order for rmmod
  LOADED_MODULES="$module $LOADED_MODULES"
done

# The network interface of a USB adapter is below its USB interface in sysfs.
i=0
while :; do
  for net in "$USB_DEV"/*/net/*; do
    if [ -e "$net" ]; then
      LAN_IFACE="${net##*/}"
      break 2
    fi
  done
  i=$((i + 1))
  if [ "$i" -ge "$LAN_ENUM_WAIT" ]; then
    fail "No network interface for $USB_DEV"
  fi
  sleep 1
done
echo "USB_ETHERNET: Using interface $LAN_IFACE"

if [ -n "$LAN_MAC" ]; then
  ifconfig "$LAN_IFACE" hw ether "$LAN_MAC" || fail "Could not set MAC $LAN_MAC"
fi
ifconfig "$LAN_IFACE" up || fail "Could not bring up $LAN_IFACE"

if [ "$MODE" = diag ]; then
  # Wi-Fi and LAN can be in the same subnet: answer ARP only on the interface
  # that has the address, and use that address as ARP source.
  echo 1 > /proc/sys/net/ipv4/conf/all/arp_ignore
  echo 2 > /proc/sys/net/ipv4/conf/all/arp_announce
  # The script sets only the address and source routing, see udhcpc-diag.script.
  # The background client keeps trying until a cable is plugged in.
  # Only one client: stop the client of an earlier run first.
  stop_diag_client "$LAN_IFACE"
  udhcpc_status=$(udhcpc -i "$LAN_IFACE" -p "/var/run/udhcpc.$LAN_IFACE.pid" -b -x hostname:"$(hostname)" \
    -s /system/sdcard/scripts/udhcpc-diag.script)
  echo "udhcpc: $udhcpc_status"
  exit 0
fi

if [ -f "$CONFIGPATH/staticip.conf" ]; then
  configure_static_net_iface "$LAN_IFACE"
else
  # The background client keeps trying until a cable is plugged in.
  udhcpc_status=$(udhcpc -i "$LAN_IFACE" -p "/var/run/udhcpc.$LAN_IFACE.pid" -b -x hostname:"$(hostname)")
  echo "udhcpc: $udhcpc_status"
fi

echo "$LAN_IFACE" > /run/net_iface
exit 0
