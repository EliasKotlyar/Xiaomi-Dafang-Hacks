#!/usr/bin/env python
import click
import os

@click.command()
@click.argument('file', default="")
def cli(file):
    dic = [
        ("kernel", 0x200000),
        ("rootfs", 0x350000),
        ("driver", 0xa0000),
        ("appfs", 0x4a0000),
    ]
    outfile = "demo_5.5.1.177.bin"
    tmpfile = "tmp.bin"
    fullflash = open(tmpfile, 'wb')
    for name, size in dic:
        filename = "5.5.1.177/" + name + ".bin"
        part = open(filename, "rb")
        buffer = part.read(size)
        fullflash.write(buffer)
    cmd = "mkimage -A MIPS -O linux -T firmware -C none -a 0 -e 0 -n jz_fw -d " + tmpfile + " " + outfile
    os.system(cmd)
    os.remove(tmpfile)


if __name__ == '__main__':
    cli()
