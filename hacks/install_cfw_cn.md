##安装microSD bootloader

1.下载相机的CFW-Binary

    名称| SHA3​​-256
    --- | ---
    [Xiaomi DaFang]（https://github.com/EliasKotlyar/Xiaomi-Dafang-Hacks/raw/master/hacks/cfw/dafang/cfw-1.3.bin）| d45826d5b471564366b3b9435509df7e8a2c0720656ea2b4bcac6dd0b42cc3eb
    [Xiaomi XiaoFang T20]（https://github.com/EliasKotlyar/Xiaomi-Dafang-Hacks/raw/master/hacks/cfw/xiaofang/cfw-1.0.bin）| 333053c3e98af24e0e90746d95e310a3c65b61f697288f974b702a5bcbba48a9
    [Wyzecam V2]（https://github.com/EliasKotlyar/Xiaomi-Dafang-Hacks/raw/master/hacks/cfw/wyzecam_v2/cfw-1.1.bin）| ca8fd695fe1903bd12aca2752c86b62c9694430c9c41b2804b006c22e84f409d
    [Wyzecam Pan]（https://github.com/EliasKotlyar/Xiaomi-Dafang-Hacks/raw/master/hacks/cfw/wyzecam_pan/cfw-1.0.bin）| f76990d187e763f160f5ad39331d6a3209d3025fe3719cb43c92dbad92cebba2
    Sannce＆clones | [从这里开始]（/ hacks / install_sannce.md）
    其他Ingenic T10 / T20设备| [从这里开始]（/ hacks / newdevices.md）

2.将microSD格式化为FAT32。 NTFS，EXFAT等不起作用。尝试使用较小的旧SD卡（如512 MB）或仅在其上创建一个主512 MB分区以获得最大成功率。

3.将步骤1中的CFW-Binary复制到格式化的microSD卡，并将其重命名为“demo.bin”。 microSD上一定不能有其他文件！这非常重要，如果那里有任何其他文件，它将无法工作。

4.从相机上拔下电源线，然后将microSD卡插入相机

5.按住相机上的设置按钮

6.插入USB电源线

7.按住设置按钮10秒钟

8.等待固件完成闪烁（例如3分钟）。一旦底座开始移动（DaFang / Wyzecam Pan），您就可以断开电源。

9.取出microSD卡并打开相机电源

10.你应该看到蓝色LED闪耀5秒钟（不闪烁）** **基地开始移动（DaFang / Wyzecam Pan）。如果没有，出了点问题。您应该尝试使用另一张microSD卡，然后查看页面底部的社区提示。从第1步开始。


##安装新固件

1.从github克隆存储库。如果您在Windows上，请将存储库下载为zip文件。确保没有任何东西获得Windows行结尾。

2.将“firmware_mod”文件夹中的所有内容复制到microSD的**根**中

它应该如下所示：
```
E：/
├──媒体
├──autoupdate.sh
├──宾
├──配置
├──对照
├──司机
├──run.sh
├──脚本
├──uEnv.bootfromnand.txt
├──uEnv.bootfromsdcard.txt
├──uboot-flash
└──www

```

3.将config / wpa_supplicant.conf.dist复制到config / wpa_supplicant.conf

4.修改microSD卡上的文件config / wpa_supplicant.conf以匹配您的wifi设置。确保wpa_supplicant.conf没有Windows行结尾。

5.插入microSD卡并打开相机电源。

6.您现在可以使用默认凭据root / ismart12登录https：// dafang或您的摄像机IP地址


提示：可以安全地忽略有关不安全的https证书的安全警告。首次启动时，相机会自动生成自签名证书。就其本质而言，您的小型相机自己的证书颁发机构并非永远不会成为主流浏览器提供的可信赖的证书。

##更新microsd-bootloader

通常，它不需要更新microsd-bootloader。但是，如果您使用的是原始固件，则可能对新版本感兴趣。

您可以通过MI-Home应用程序进行更新。


如果您的原始固件低于5.5.200，则必须在之后“重新刷新”microsd-bootloader

如果您使用的是原始固件5.5.200并更新到5.5.243，则引导加载程序不会受到影响。



##更新固件

如果您已安装了安装了自定义引导加载程序的当前自定义固件，则只需更新microSD卡的内容即可

1.备份你的wpa_config / wpa_supplicant.conf

2.从microSD卡中删除所有文件

3.将“firmware_mod”文件夹中的所有内容放入microSD卡的**根**中

4.将备份的wpa_supplicant.conf从步骤1复制回config文件夹


##卸载

从microSD卡中删除“run.sh”文件。

##社区提示

1.使用小于1 GB的microSD卡（如512 MB）并覆盖相同的卡以最大限度地减少变化。仅格式化前512 MB也适用于某些人。

2.如果引导加载程序步骤不起作用，请再次检查microSD卡上是否有库存固件创建的文件或文件夹。 （有时如果按照设置关闭时间，相机将创建一个时间戳相关文件夹，需要在再次尝试之前删除）。

3.记下摄像机的MAC，如果可能，设置DHCP以分配可在DHCP日志中直观监视的特定IP地址。

4.从wpa_supplicant.conf中的较少条目开始，以隔离WiFi问题。
```
ctrl_interface =的/ var /运行/的wpa_supplicant
ctrl_interface_group = 0
ap_scan = 1

网络