# Additional instructions for T20L users

The Xiaofang T20L is different from the T20, which requires some more steps to get the CFW running from SD card. 

## Installation of the bootloader

The cfw-1.0 bootloader used on the T20 is compatible with the T20L. So follow the [installation instructions](/hacks/install_cwf.md)
for installation of the bootloader (this is the first part of the installation instruction).

## Installation of the firmware

There is an additional step required for the T20L. First, clone the repository from github. If you are on Windows download the repository as zip file.
Make sure nothing gets windows line endings.

Inside the `firmware_mod` folder, there are two files called `uEnv.bootfromnand.txt` and `uEnv.bootfromsdcard.txt`. **Delete** those files and rename the
`uEnv.bootfromnand.t20l.txt` to `uEnv.bootfromnand.txt` and `uEnv.bootfromsdcard.t20l.txt` to `uEnv.bootfromsdcard.txt`. Effectively, you replace the
existing uEnv files with the two modified specifically for the T20L.

Next, inside the `firmware_mod` folder, there is a `driver` folder and a `driver_t20l` folder. Copy all files from `driver_t20l` and copy those into the
`driver` folder. Make sure to **overwrite** any existing file to replace them with the proper drivers.

Now you can continue with step 2 from the [firmware installation instructions](/hacks/install_cfw.md#installation-of-the-new-firmware) by copying the
contents to the SD card and further following the instructions.
