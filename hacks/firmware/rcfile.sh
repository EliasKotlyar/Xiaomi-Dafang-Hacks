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

i="0"
while 1
do
    if [ -f /dev/mmcblk0p1 ]; then
        mount /dev/mmcblk0p1 /system/sdcard
        if [ -f /system/sdcard/run.sh ]; then
	        /system/sdcard/run.sh &
	    fi
        break
    elif [ $i -gt 5 ]; then
        break
    fi
   sleep 1
   i=$[$i+1]
done


if [ -f /system/init/app_init.sh ]; then
    /system/init/app_init.sh &
fi
