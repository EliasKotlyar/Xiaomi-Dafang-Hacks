### Getting Root access from the Serial
1. Boot into Uboot(press a Key when booting)
2. Use the following Command to get a Root-Shell

`setenv bootargs console=ttyS1,115200n8 mem=104M@0x0 ispmem=8M@0x6800000 rmem=16M@0x7000000 init=/bin/sh rootfstype=squashfs root=/dev/mtdblock2 rw mtdparts=jz_sfc:256k(boot),2048k(kernel),3392k(root),640k(driver),4736k(appfs),2048k(backupk),640k(backupd),2048k(backupa),256k(config),256k(para),-(flag)`

3. Boot into the Root-Shell using "boot"

