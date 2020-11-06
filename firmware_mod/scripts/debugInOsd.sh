#!/bin/sh
IF=wlan0

while true
do
	R1=`cat /sys/class/net/${IF}/statistics/rx_bytes`
	T1=`cat /sys/class/net/${IF}/statistics/tx_bytes`
	sleep 1
	R2=`cat /sys/class/net/${IF}/statistics/rx_bytes`
	T2=`cat /sys/class/net/${IF}/statistics/tx_bytes`
	TBPS=$(($T2-$T1))
	RBPS=$(($R2-$R1))
	TKBPS=$(($TBPS/1024))
	RKBPS=$(($RBPS/1024))
	IP=`ifconfig | sed -En 's/127.0.0.1//;s/.*inet (addr:)?(([0-9]*\.){3}[0-9]*).*/\2/p'`
#	CPU=`grep 'cpu ' /proc/stat | awk '{ printf("%.0f", ($2+$4)*100/($2+$4+$5)) }'`
	CPU=`top -n 1 | grep CPU: | grep -v grep| awk '{ print $2}'`
	freemem=`free | grep Mem |grep -v grep | awk '{ printf("%.0f", $4/$2 * 100.0) }'`
	memtop=`top -n 1 | grep Mem: |grep -v grep |  awk '{ printf("Used=%.0fk Free=%.0fk",$2,$4)}'`
	string="`hostname`  ${IP}  tx:$TKBPS kb/s  rx:$RKBPS kb/s  CPU=${CPU}%   FreeMem=${freemem}% ${memtop}"
#	echo ".$string." >> /var/log/osd
	/system/sdcard/bin/setconf -k o -v "${string}"

done
