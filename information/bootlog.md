```
eko@eko-GE62VR-6RF:~$ picocom -b 115200 /dev/ttyUSB0
picocom v2.2

port is        : /dev/ttyUSB0
flowcontrol    : none
baudrate is    : 115200
parity is      : none
databits are   : 8
stopbits are   : 1
escape is      : C-a
local echo is  : no
noinit is      : no
noreset is     : no
nolock is      : no
send_cmd is    : sz -vv
receive_cmd is : rz -vv -E
imap is        :
omap is        :
emap is        : crcrlf,delbs,

Type [C-a] [C-h] to see available commands

Terminal ready

U-Boot SPL 2013.07 (Jul 28 2017 - 17:10:01)
pll_init:365
l2cache_clk = 375000000
pll_cfg.pdiv = 8, pll_cfg.h2div = 4, pll_cfg.h0div = 4, pll_cfg.cdiv = 1, pll_cfg.l2div = 3
nf=36 nr = 1 od0 = 1 od1 = 1
cppcr is 02404900
CPM_CPAPCR 0470890d
nf=42 nr = 1 od0 = 1 od1 = 1
cppcr is 02a04900
CPM_CPMPCR 07d0c90d
nf=50 nr = 1 od0 = 1 od1 = 1
cppcr is 03204900
CPM_CPVPCR 0320490d
cppcr 0x9a794410
apll_freq 860160000
mpll_freq 1000000000
vpll_freq = 1200000000
ddr sel mpll, cpu sel apll
ddrfreq 500000000
cclk  860160000
l2clk 286720000
h0clk 250000000
h2clk 250000000
pclk  125000000
DDRC_DLP:0000f003


U-Boot 2013.07 (Jul 28 2017 - 17:10:01)

Board: ISVP (Ingenic XBurst T20 SoC)
DRAM:  128 MiB
Top of RAM usable for U-Boot at: 84000000
Reserving 399k for U-Boot at: 83f9c000
Reserving 32784k for malloc() at: 81f98000
Reserving 32 Bytes for Board Info at: 81f97fe0
Reserving 124 Bytes for Global Data at: 81f97f64
Reserving 128k for boot params() at: 81f77f64
Stack Pointer at: 81f77f48
Now running in RAM - U-Boot at: 83f9c000
MMC:   msc: 0
the manufacturer c8
SF: Detected GD25Q128

*** Warning - bad CRC, using default environment

In:    serial
Out:   serial
Err:   serial
misc_init_r before change the yellow_gpio
gpio_request lable = yellow_gpio gpio = 38
misc_init_r after gpio_request the yellow_gpio ret is 38
misc_init_r after change the yellow_gpio ret is 0
misc_init_r before change the blue_gpio
gpio_request lable = blue_gpio gpio = 39
misc_init_r after gpio_request the blue_gpio ret is 39
misc_init_r after change the blue_gpio ret is 1
gpio_request lable = night_gpio gpio = 81
misc_init_r after gpio_request the night_gpio ret is 81
misc_init_r after change the night_gpio ret is 0
gpio_request lable = night_gpio gpio = 25
misc_init_r after gpio_request the night_gpio ret is 25
misc_init_r after change the night_gpio ret is 0
gpio_request lable = night_gpio gpio = 49
misc_init_r after gpio_request the night_gpio ret is 49
misc_init_r after change the night_gpio ret is 0
gpio_request lable = USB_able_gpio gpio = 47
misc_init_r after gpio_request the USB_able_gpio ret is 47
misc_init_r after change the USB_able_gpio ret is 1
gpio_request lable = TF_able_gpio gpio = 43
misc_init_r after gpio_request the TF_able_gpio ret is 43
misc_init_r after change the TF_able_gpio ret is 1
gpio_request lable = SPK_able_gpio gpio = 63
misc_init_r after gpio_request the SPK_able_gpio ret is 63
misc_init_r after change the SPK_able_gpio ret is 0
gpio_request lable = SD_able_gpio gpio = 48
misc_init_r after gpio_request the SD_able_gpio ret is 48
misc_init_r after change the SD_able_gpio ret is 0
Hit any key to stop autoboot:  0
isvp_t20#
FATAL: term closed
eko@eko-GE62VR-6RF:~$
```
