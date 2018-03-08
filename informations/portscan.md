## Software Infos:

Opened Ports:
1. Port 80: Probably "Boa HTTPd 0.94.13" according to Nmap
2. Port 10002 : No Clue yet, but it responds with the following Sequence if you send a simple
"GET"-Request:

ICAM�������������ÿ����s���àÖÑv�����TÑv

The complete portscan:
```
Starting Nmap 7.60 ( https://nmap.org ) at 2017-10-20 22:16 CEST
NSE: Loaded 146 scripts for scanning.
NSE: Script Pre-scanning.
Initiating NSE at 22:17
Completed NSE at 22:17, 0.00s elapsed
Initiating NSE at 22:17
Completed NSE at 22:17, 0.00s elapsed
Initiating ARP Ping Scan at 22:17
Scanning 192.168.0.98 [1 port]
Completed ARP Ping Scan at 22:17, 0.21s elapsed (1 total hosts)
Initiating Parallel DNS resolution of 1 host. at 22:17
Completed Parallel DNS resolution of 1 host. at 22:17, 13.00s elapsed
Initiating SYN Stealth Scan at 22:17
Scanning 192.168.0.98 [1000 ports]
Discovered open port 80/tcp on 192.168.0.98
Discovered open port 10002/tcp on 192.168.0.98
Increasing send delay for 192.168.0.98 from 0 to 5 due to 362 out of 904 dropped probes since last increase.
Increasing send delay for 192.168.0.98 from 5 to 10 due to 117 out of 292 dropped probes since last increase.
Completed SYN Stealth Scan at 22:17, 6.66s elapsed (1000 total ports)
Initiating Service scan at 22:17
Scanning 2 services on 192.168.0.98
Completed Service scan at 22:19, 151.27s elapsed (2 services on 1 host)
Initiating OS detection (try #1) against 192.168.0.98
adjust_timeouts2: packet supposedly had rtt of -193196 microseconds.  Ignoring time.
adjust_timeouts2: packet supposedly had rtt of -193196 microseconds.  Ignoring time.
NSE: Script scanning 192.168.0.98.
Initiating NSE at 22:19
Completed NSE at 22:19, 0.21s elapsed
Initiating NSE at 22:19
Completed NSE at 22:19, 1.01s elapsed
Nmap scan report for 192.168.0.98
Host is up (0.0030s latency).
Not shown: 998 closed ports
PORT      STATE SERVICE     VERSION
80/tcp    open  http        Boa HTTPd 0.94.13
| http-methods:
|_  Supported Methods: GET HEAD POST
|_http-server-header: Boa/0.94.13
|_http-title: Site doesn't have a title (text/html).
10002/tcp open  documentum?
MAC Address: 34:CE:XX:XX:XX:XX (Xiaomi Electronics,co.)
Device type: general purpose
Running: Linux 2.6.X|3.X
OS CPE: cpe:/o:linux:linux_kernel:2.6 cpe:/o:linux:linux_kernel:3
OS details: Linux 2.6.32 - 3.10
Uptime guess: 0.003 days (since Fri Oct 20 22:14:55 2017)
Network Distance: 1 hop
TCP Sequence Prediction: Difficulty=247 (Good luck!)
IP ID Sequence Generation: All zeros

TRACEROUTE
HOP RTT     ADDRESS
1   3.05 ms 192.168.0.98

NSE: Script Post-scanning.
Initiating NSE at 22:19
Completed NSE at 22:19, 0.00s elapsed
Initiating NSE at 22:19
Completed NSE at 22:19, 0.00s elapsed
Read data files from: /usr/bin/../share/nmap
OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 175.08 seconds
           Raw packets sent: 1693 (76.940KB) | Rcvd: 1227 (51.488KB)
```
