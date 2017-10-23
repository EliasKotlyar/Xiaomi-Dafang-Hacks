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
dd if=/dev/mtdblock0 of=uboot.bin bs=262144
dd if=/dev/mtdblock1 of=kernel.bin bs=2097152
dd if=/dev/mtdblock2 of=rootfs.bin bs=3473408
dd if=/dev/mtdblock3 of=driver.bin bs=655360
dd if=/dev/mtdblock4 of=appfs.bin bs=4849664
dd if=/dev/mtdblock5 of=backupk.bin bs=2097152
dd if=/dev/mtdblock6 of=backupd.bin bs=655360
dd if=/dev/mtdblock7 of=backupa.bin bs=2097152
dd if=/dev/mtdblock8 of=config.bin bs=262144
dd if=/dev/mtdblock9 of=para.bin bs=262144
dd if=/dev/mtdblock10 of=flag.bin bs=65536
```




## Extract Kernel:
The Kernel is compressed using lzma. Use the following Instructions for extracting it:
https://stackoverflow.com/questions/37672417/getting-kernel-version-from-the-compressed-kernel-image


## Extract AppFS:
Use following Tutorial:
https://integriography.wordpress.com/2015/03/16/mounting-a-jffs2-dd-image-in-linux/
