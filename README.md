## Xiaomi Dafang Hacks

This repository is a collection of informations&software for the Dafang Camera

![Dafang](/dafang.png)


## Informations:
[Teardown](/teardown)
[Hardware](/informations/hardware.md)
[Portscan of original Software](/informations/portscan.md)

## Hacks
[Installation of Serial-Headers](/mod_serial)
[Getting Root-Access using Serial](/mod_getroot/getroot.md)
[Dumping-Firmware](/mod_getroot/firmware-dump.md)
[Installing Telnet & configuring Wifi](/mod_getroot/install_telnetandwifi.md)



## Contribution

Any contribution to the development is highly welcome. The best possibility to provide any change is to open a pull request on GitHub.





## Software Infos:

Opened Ports:
1. Port 80: Probably "Boa HTTPd 0.94.13" according to Nmap
2. Port 10002 : No Clue yet, but it responds with the following Sequence if you send a simple
"GET"-Request:

ICAM�������������ÿ����s���àÖÑv�����TÑv

The complete portscan can be found in portscan.txt

## Testpoints on Board:

![Headers](/teardown/headers_sample.jpg)

have a look at mod_serial folder for a example setup of the serial-console

## Hardware required for debugging:
FTDI-Adapter with 3.3V




## List of sources:
A Hack of a similar Device(Camera using the Ingenico T10):

[Part1](http://nm-projects.de/2016/12/hacking-digoo-bb-m2-mini-wifi-part-1-identify-the-serial-interface/)
[Part2](http://nm-projects.de/2017/01/hacking-ip-camera-digoo-bb-m2-part-2-analyzing-the-boot-process/)
[Part3](http://nm-projects.de/2017/01/hacking-ip-camera-digoo-bb-m2-part-3-getting-root-access/)

Linux on Ingenic Devices:

[Linus Mips](https://www.linux-mips.org/wiki/Ingenic)


