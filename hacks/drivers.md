Adding of Sensor:
```
insmod /driver/sensor_jxf22.ko data_interface=2 pwdn_gpio=-1 reset_gpio=18 sensor_gpio_func=0
```


Get information about the Sensor:

Get Info about the Sensor:
echo 1 >/proc/jz/sinfo/info


Enable more RAM:
```

echo 100 > /proc/sys/vm/swappiness
echo 16777216 > /sys/block/zram0/disksize
mkswap /dev/zram0
swapon /dev/zram0

```

Params of the Motor:
```
Insmod Motor:
hmaxstep = 2600
hmotor2vmotor = 1
vmaxstep = 700
```
