#!/usr/bin/env python
import click


@click.command()
@click.argument('file', default="")
def cli(file):
    dic = [
        ("kernel", 0x200000),
        ("rootfs", 0x350000),
        ("driver", 0xa0000),
        ("appfs", 0x4a0000),
    ]
    file = "demo_5.5.1.194.bin"
    fullflash = open(file, 'rb')
    fullflash.seek(64)
    for name, size in dic:
        filename = "flash/" + name + ".bin"
        buffer = fullflash.read(size)
        f = open(filename, "wb")
        f.write(buffer)


if __name__ == '__main__':
    cli()
