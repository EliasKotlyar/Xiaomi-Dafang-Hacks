This page explains what the `mem=41700K@0x0 ispmem=8M@0x28B9000 rmem=15644K@0x30B9000` kernel cmdline arguments mean.


**1. Why is there only 35404KB `TotalMem` even though 41700K are specified?**
Some space is taken by the kernel:
```
Memory: 35192k/41700k available (3951k kernel code, 6508k reserved, 1276k data, 212k init, 0k highmem)
```
I think the 212k init make up the difference to the `35404KB` total:
```
[    1.663642] Freeing unused kernel memory: 212K
```

**2. What are ispmem/rmem actually used for?**

According to https://github.com/Dafang-Hacks/Ingenic-T10_20/blob/master/doc.7z:

> 3. 预留内存及内核裁减
> 
> 预留内存分为两部分：ispmem及rmem：
> 
> * ispmem为ISP所需内存，计算方法为Sensor输出图像长x宽x4，例如对于720P的Sensor为1280x720x4=3600KB，对于960P的Sensor为1280x960x4=4800KB。若需要打开WDR功能，ispmem需要2倍的大小（即长x宽x4x2）。
> * rmem为系统Video Buffer所需内存，720P大概需要14MB内存，960P大概需要19M内存。

which roughly translates to:

> 3. Reserved memory
> 
> The reserved memory is divided into two parts: ispmem and rmem:
> 
> * ispmem is the memory required by the ISP, and the calculation method is Sensor output image length x width x4, for example, 1280x720x4 = 3600KB for 720P Sensor, 1280x960x4 = 4800KB for 960P Sensor. If you need to turn on the WDR function, ispmem needs twice the size (ie length x width x4x2).
> * rmem is the memory required by the system Video Buffer, 720P requires 14MB memory, 960P requires 19M memory.

`WDR` means Wide Dynamic Range (like HDR), which we are not using. So according to this, `8100KB` (=7,91MB) ispmem would be necessary for 1080p.
`isp` means the `Image Signal Processor` of the T20:
![image](https://user-images.githubusercontent.com/801996/79064105-63436d00-7ca6-11ea-8ad1-013328c6ea89.png)


I had a really hard time finding out where these cmdline parameters are actually used in the kernel. I see no reason not to trust these values in the docs, but I'd like to know how this really works.

In `arch/mips/xburst/soc-t20/common/platform.c`:,  `__setup("ispmem=", ispmem_parse);` sets `ispmem_size` and `ispmem_base` variables, but these are not used anywhere else in the kernel.

Ingenic-specific [rmem.c](https://github.com/Dafang-Hacks/kernel/blob/master/drivers/misc/rmem.c) creates a `/dev/rmem` device which is an exclusive memory region to be used by `libimp`. 
Accordingly, v4l2rtspserver fails to start when all memory is used for user-space memory and ispmem. There are no references to `rmem` in the v4l2 code either though.

Use `pmap $(pidof v4l2rtspserver-master) |grep rmem` to examine the `rmem` memory usage.

**3. What's up with the memory region marked `usable after init`  in the boot log?**
The (automatically) "determined physical RAM map" is never used because we specify a user-defiend physical RAM map:

```
[    0.000000] Determined physical RAM map:  <--- this is automatically determined
[    0.000000]  memory: 0051b000 @ 00010000 (usable)
[    0.000000]  memory: 00035000 @ 0052b000 (usable after init)
[    0.000000] User-defined physical RAM map: <- this overwrites the automatically determined memory maps
[    0.000000]  memory: 028b9000 @ 00000000 (usable)
```

