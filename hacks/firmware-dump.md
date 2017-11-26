# Dumping Firmware:

## The Partition Table:
```
[root@Ingenic-uc1_1:dev]# cat /proc/mtd 
dev:    size   erasesize  name
mtd0: 00040000 00008000 "boot"
mtd1: 00200000 00008000 "kernel"
mtd2: 00350000 00008000 "root"
mtd3: 000a0000 00008000 "driver"
mtd4: 004a0000 00008000 "appfs"
mtd5: 00200000 00008000 "backupk"
mtd6: 000a0000 00008000 "backupd"
mtd7: 00200000 00008000 "backupa"
mtd8: 00040000 00008000 "config"
mtd9: 00040000 00008000 "para"
mtd10: 00010000 00008000 "flag"
```

Attention: The Values are in Hex. Convert into Decimal for using DD
`

## Dump everything:
```
dd if=/dev/mtdblock0 of=uboot.bin 
dd if=/dev/mtdblock1 of=kernel.bin
dd if=/dev/mtdblock2 of=rootfs.bin 
dd if=/dev/mtdblock3 of=driver.bin 
dd if=/dev/mtdblock4 of=appfs.bin 
dd if=/dev/mtdblock5 of=backupk.bin 
dd if=/dev/mtdblock6 of=backupd.bin 
dd if=/dev/mtdblock7 of=backupa.bin
dd if=/dev/mtdblock8 of=config.bin 
dd if=/dev/mtdblock9 of=para.bin 
dd if=/dev/mtdblock10 of=flag.bin
```




