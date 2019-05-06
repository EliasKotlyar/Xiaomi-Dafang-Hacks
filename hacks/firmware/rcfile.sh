#!/bin/sh

# Set mdev
echo /sbin/mdev > /proc/sys/kernel/hotplug
/sbin/mdev -s && echo "mdev is ok......"

# create console and null node for nfsroot
#mknod -m 600 /dev/console c 5 1
#mknod -m 666 /dev/null c 1 3

# Set Global Environment
export PATH=/bin:/sbin:/usr/bin:/usr/sbin
export PATH=/system/bin:$PATH
export LD_LIBRARY_PATH=/system/lib
export LD_LIBRARY_PATH=/thirdlib:$LD_LIBRARY_PATH

# networking
ifconfig lo up
#ifconfig eth0 192.168.1.80

# Start telnet daemon
telnetd &

# Set the system time from the hardware clock
#hwclock -s

#set the GPIO PC13 to high, make the USB Disk can be use
cd /sys/class/gpio
echo 77 > export       #申请GPIO
cd gpio77
echo out > direction   #设置为输出模式
echo 0 > active_low    #value是0,表示低电平。value是1,表示高电平
echo 1 > value         #设置电平（输出模式）

# Mount driver partition
mount -t squashfs /dev/mtdblock3 /driver

# Mount system partition
mount -t jffs2 /dev/mtdblock4 /system

# Mount backup partition
#mount -t jffs2 /dev/mtdblock5 /backupk

# Mount backup partition
#mount -t jffs2 /dev/mtdblock6 /backupd

# Mount backup partition
mount -t jffs2 /dev/mtdblock7 /backupa

# Mount configs partition
mount -t jffs2 /dev/mtdblock8 /configs

# Mount params partition
mount -t jffs2 /dev/mtdblock9 /params

# Format system patition if it is invalid
if [ ! -f /system/.system ]; then
    echo "Format system partition..."
    umount -f /system
    flash_eraseall /dev/mtd4
    mount -t jffs2 /dev/mtdblock4 /system
    cd /system
    mkdir -p bin init etc/sensor lib/firmware lib/modules
    echo "#!/bin/sh" > init/app_init.sh
    chmod 755 init/app_init.sh
    touch .system
    cd /
    echo "Done"
fi


# Turn on blue LED
echo 39 > /sys/class/gpio/export
echo out > /sys/class/gpio/gpio39/direction
echo 0 > /sys/class/gpio/gpio39/active_low
echo 0 > /sys/class/gpio/gpio39/value
# Check if we're on a Wyzecam and properly enable the SD card interface
if [ -f /driver/rtl8189ftv.ko ]; then
    echo 43 >/sys/class/gpio/export
    echo out >/sys/class/gpio/gpio43/direction
    echo 0 >/sys/class/gpio/gpio43/value
fi
i="0"
while true
do
    echo "Trying to mount SDCard..."
    if [ -e /dev/mmcblk0p1 ]; then
        mkdir /system/sdcard
        mount /dev/mmcblk0p1 /system/sdcard
        sleep 1
        echo "Mount sucessful"
        if [ -f /system/sdcard/run.sh ]; then
            echo 1 > /sys/class/gpio/gpio39/value
            echo 39 > /sys/class/gpio/unexport
            echo "Starting run.sh from sdcard"
            /system/sdcard/run.sh &
            exit 0
        fi
	echo "Couldnt find run.sh, starting normal..."
	umount /system/sdcard
        break
    elif [ $i -gt 5 ]; then
        echo "Couldnt mount, starting normal..."
        break
    fi
    sleep 1
    let i=i+1
done
# Turn off blue LED
echo 1 > /sys/class/gpio/gpio39/value
echo 39 > /sys/class/gpio/unexport


if [ -f /system/init/app_init.sh ]; then
    /system/init/app_init.sh &
fi
