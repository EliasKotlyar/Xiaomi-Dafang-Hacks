## Infos

## Some Information about the System:
```
[root@Ingenic-uc1_1:mmc]# cat /proc/cpuinfo 
system type		: bull
machine			: Unknown
processor		: 0
cpu model		: Ingenic Xburst V0.1  FPU V0.0
BogoMIPS		: 858.52
wait instruction	: yes
microsecond timers	: no
tlb_entries		: 32
extra interrupt vector	: yes
hardware watchpoint	: yes, count: 1, address/irw mask: [0x0fff]
isa			: mips32r1
ASEs implemented	:
shadow register sets	: 1
kscratch registers	: 7
core			: 0
VCED exceptions		: not available
VCEI exceptions		: not available

Hardware		: isvp
Serial			: 00000000 00000000 00000000 00000000

Attention:
It is a little-Endian System


```

Here is a 


```
Add Sensor:

 insmod /driver/sensor_jxf22.ko data_interface=2 pwdn_gpio=-1 reset_gpio=18 sensor_gpio_func=0


Insmod Motor:
hmaxstep = 2600
hmotor2vmotor = 1
vmaxstep = 700


Get Info about the Sensor:
echo 1 >/proc/jz/sinfo/info



echo 100 > /proc/sys/vm/swappiness
echo 16777216 > /sys/block/zram0/disksize
mkswap /dev/zram0
swapon /dev/zram0


```
