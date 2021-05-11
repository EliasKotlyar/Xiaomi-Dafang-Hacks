#!/bin/sh

export LD_LIBRARY_PATH='/system/sdcard/lib/:/thirdlib:/system/lib'

CONFIGPATH="/system/sdcard/config"
LOGDIR="/system/sdcard/log"
LOGPATH="$LOGDIR/startup.log"
if [ ! -d $LOGDIR ]; then
  mkdir -p $LOGDIR
fi
echo "==================================================" >> $LOGPATH
echo "Starting the Dafang Hacks Custom Application Layer" >> $LOGPATH
echo "==================================================" >> $LOGPATH

## Stop telnet for security reasons
killall telnetd

## Load some common functions:
. /system/sdcard/scripts/common_functions.sh
echo "Loaded common functions" >> $LOGPATH

## Create root user home directory and etc directory on sdcard:
if [ ! -d /system/sdcard/root ]; then
  mkdir /system/sdcard/root
  echo 'PATH=/system/sdcard/bin:$PATH' > /system/sdcard/root/.profile
  echo "Created root user home directory" >> $LOGPATH
fi
mkdir -p /system/sdcard/etc
while IFS= read -r etc_element
do
  if [ ! -f "/system/sdcard/etc/$etc_element" ] && [ ! -d "/system/sdcard/etc/$etc_element" ]; then
    cp -fRL "/etc/$etc_element" /system/sdcard/etc
  fi
done <<- END
	TZ
	protocols
	fstab
	inittab
	init.d
	hosts
	group
	resolv.conf
	hostname
	profile
	os-release
	sensor
	webrtc_profile.ini
END
echo "Created etc directory on sdcard" >> $LOGPATH

mount -o bind /system/sdcard/bin/busybox /bin/busybox
echo "Bind mounted /system/sdcard/bin/busybox to /bin/busybox" >> $LOGPATH
mount -o bind /system/sdcard/root /root
echo "Bind mounted /system/sdcard/root to /root" >> $LOGPATH
mount -o bind /system/sdcard/etc /etc
echo "Bind mounted /system/sdcard/etc to /etc" >> $LOGPATH

## Create busybox aliases
if [ ! -f ~/.busybox_aliases ]; then
  /system/sdcard/bin/busybox --list | sed "s/^\(.*\)$/alias \1='busybox \1'/" > ~/.busybox_aliases
fi

if [ -f "$CONFIGPATH/swap.conf" ]; then
  . $CONFIGPATH/swap.conf
fi

## Create a swap file on SD if desired
if [ "$SWAP" = true ]; then
  if [ ! -f $SWAPPATH ]; then
    echo "Creating ${SWAPSIZE}MB swap file on SD card"  >> $LOGPATH
    dd if=/dev/zero of=$SWAPPATH bs=1M count=$SWAPSIZE
    mkswap $SWAPPATH
    echo "Swap file created in $SWAPPATH" >> $LOGPATH
  fi
  echo "Configuring swap file" >> $LOGPATH
  swapon -p 10 $SWAPPATH
  echo "Swap set on file $SWAPPATH" >> $LOGPATH
fi

# Create ZRAM swap as on the original firmware
if [ ! "$SWAP_ZRAM" = false ]; then
    echo 100 > /proc/sys/vm/swappiness
    echo $SWAP_ZRAM_SIZE > /sys/block/zram0/disksize
    mkswap /dev/zram0
    swapon -p 20 /dev/zram0
fi

## Create cron periodic dirs and start crond:
CRONPERIODIC="${CONFIGPATH}/cron/periodic"
if [ ! -d $CRONPERIODIC ]; then
  mkdir -p ${CRONPERIODIC}/15min \
           ${CRONPERIODIC}/hourly \
           ${CRONPERIODIC}/daily \
           ${CRONPERIODIC}/weekly \
           ${CRONPERIODIC}/monthly
  echo "Created cron periodic directories" >> $LOGPATH
fi
/system/sdcard/bin/busybox crond -L /system/sdcard/log/crond.log -c /system/sdcard/config/cron/crontabs

## Set Hostname
if [ ! -f $CONFIGPATH/hostname.conf ]; then
  cp $CONFIGPATH/hostname.conf.dist $CONFIGPATH/hostname.conf
fi
hostname -F $CONFIGPATH/hostname.conf

## Load network driver
if [ -f $CONFIGPATH/usb_eth_driver.conf ]; then
  ## Start USB Ethernet:
  echo "USB_ETHERNET: Detected USB config. Loading USB Ethernet driver" >> $LOGPATH
  insmod /system/sdcard/driver/usbnet.ko
  insmod /system/sdcard/driver/asix.ko

  ## Configure network address
  if [ -f "$CONFIGPATH/staticip.conf" ]; then
    configure_static_net_iface eth0 >> $LOGPATH
  else
    # Configure with DHCP client
    ifconfig eth0 up
    udhcpc_status=$(udhcpc -i eth0 -p /var/run/udhcpc.eth0.pid -b -x hostname:"$(hostname)")
    echo "udhcpc: $udhcpc_status" >> $LOGPATH
  fi
else
  ## Start Wifi:
  MAC=$(get_wifi_mac)
  if [ -f /driver/8189es.ko ]; then
    # Its a DaFang
    insmod /driver/8189es.ko rtw_initmac="$MAC"
  elif [ -f /driver/8189fs.ko ]; then
    # Its a XiaoFang T20
    insmod /driver/8189fs.ko rtw_initmac="$MAC"
  else
    # Its a Wyzecam V2
    insmod /driver/rtl8189ftv.ko rtw_initmac="$MAC"
  fi
  /system/sdcard/scripts/wifi.sh start >> $LOGPATH
fi

## Set Timezone
set_timezone

## Sync the time via NTP:
if [ ! -f $CONFIGPATH/ntp_srv.conf ]; then
  cp $CONFIGPATH/ntp_srv.conf.dist $CONFIGPATH/ntp_srv.conf
fi
ntp_srv="$(cat "$CONFIGPATH/ntp_srv.conf")"
timeout 30 sh -c "until ping -c1 \"$ntp_srv\" &>/dev/null; do sleep 3; done";
/system/sdcard/bin/busybox ntpd -p "$ntp_srv"

## Load audio driver module:
insmod /system/sdcard/driver/audio.ko

## Initialize the GPIOS:
for pin in 25 26 38 39 49; do
  init_gpio $pin
done
# the ir_led pin is a special animal and needs active low
echo 1 > /sys/class/gpio/gpio49/active_low

echo "Initialized gpios" >> $LOGPATH

## Set leds to default startup states:
## LED's off by default to inscrease camera stealth
ir_led off
ir_cut on
yellow_led off
blue_led off

## Load motor driver module:
insmod /driver/sample_motor.ko

## Determine the image sensor model:
insmod /system/sdcard/driver/sinfo.ko
echo 1 >/proc/jz/sinfo/info
sensor=$(grep -m1 -oE 'jxf[0-9]*$' /proc/jz/sinfo/info)
echo "Determined image sensor model as $sensor" >> $LOGPATH

## Start the image sensor:
insmod /driver/tx-isp.ko isp_clk=100000000
if [ $sensor = 'jxf22' ]; then
  insmod /driver/sensor_jxf22.ko data_interface=2 pwdn_gpio=-1 reset_gpio=18 sensor_gpio_func=0
else
  if [ ! -f /etc/sensor/jxf23.bin ]; then
    cp /etc/sensor/jxf22.bin /etc/sensor/jxf23.bin
    cp /etc/sensor/jxf22move.txt /etc/sensor/jxf23move.txt
  fi
  insmod /system/sdcard/driver/sensor_jxf23.ko data_interface=2 pwdn_gpio=-1 reset_gpio=18 sensor_gpio_func=0
fi

## Copy autonight configuration:
if [ ! -f $CONFIGPATH/autonight.conf ]; then
  cp $CONFIGPATH/autonight.conf.dist $CONFIGPATH/autonight.conf
fi

## Copy onvif camera ptz configuration:
if [ ! -f $CONFIGPATH/ptz_presets.conf ]; then
  cp $CONFIGPATH/ptz_presets.conf.dist $CONFIGPATH/ptz_presets.conf
fi

## Configure OSD:
if [ -f /system/sdcard/controlscripts/configureOsd ]; then
    . /system/sdcard/controlscripts/configureOsd  2>/dev/null
fi

## Configure Motion:
if [ -f /system/sdcard/controlscripts/configureMotion ]; then
    . /system/sdcard/controlscripts/configureMotion  2>/dev/null
fi

## Autostart all enabled services:
for i in /system/sdcard/config/autostart/*; do
  $i &
done

## Autostart startup userscripts
/bin/find /system/sdcard/config/userscripts/startup/ -executable -name "*.sh" -exec {} \;

echo "Startup finished!" >> $LOGPATH
echo "" >> $LOGPATH
echo "Contents of dmesg after startup:" >> $LOGPATH
dmesg >> $LOGPATH
