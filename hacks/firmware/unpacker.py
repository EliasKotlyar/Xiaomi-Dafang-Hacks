#!/usr/bin/env python
# coding=utf-8
import click

import os
CHECK_FOLDER = os.path.isdir("flash")
if not CHECK_FOLDER:
    os.makedirs("flash")

@click.command()
@click.argument('inputfile', default="demo_5.5.1.194.bin", type=click.Path(exists=True))
def cli(inputfile):
    dic = [
        ("kernel", 0x200000),
        ("rootfs", 0x350000),
        ("driver", 0xa0000),
        ("appfs", 0x4a0000),
    ]
    inputfile = click.format_filename(inputfile)
    fullflash = open(inputfile, 'rb')
    fullflash.seek(64)
    for name, size in dic:
        filename = "flash/" + name + ".bin"
        buffer = fullflash.read(size)
        f = open(filename, "wb")
        f.write(buffer)


if __name__ == '__main__':
    cli()
