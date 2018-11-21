

## Install new Version using the SD-Card
```$xslt
flash_eraseall /dev/mtd4
dd if=appfs.bin of=/dev/mtd4
```


### Install new Version using the Bootloader:
```$xslt
fatls mmc 0:1
fatload mmc 0:1 0x80600000 dafang_128mb_v2.bin
sf probe
sf update 0x80600000 0x0 0x40000

```