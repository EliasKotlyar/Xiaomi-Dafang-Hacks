## Xiaomi Dafang Integration in Zoneminder

ZM Setup:

Click "Add a Monitor"
### General Tab

Name your camera

Select Source Type of "FFmpeg"

Function (this depends on you, I picked modect)

Left all other settings as-is on this tab
![pic](Screenshot%202018-04-30%2011.50.15.png)

### Source Tab

Source Path: rtsp://XX.XX.XX.XX:8554/unicast (Where XX.XX.XX.XX is the IP of your camera)

Remote Method: UDP (This was the first I tired and it worked, not saying it's the only way.

Target colorspace: 32 bit colour

Capture Width: 1920

Capture Height: 1080

The rest as-is ![pic](Screenshot%202018-04-30%2011.52.42.png)
BEFORE you can configure the Control tab

If you don't see this make sure you enabled OPT_CONTROL in the ZM options.
Copy [Xiaomi.pm](https://github.com/EliasKotlyar/Xiaomi-Dafang-Hacks/blob/master/integration/zoneminder/Xiaomi.pm) into a file named Xiaomi.pm in /usr/share/perl5/ZoneMinder/Control/ (May be different for your distro, make sure it has the same permissions as the other controls)

Navigate to the control tab for your camera

Click on the "Edit" next to "Control Type"

Click "Add New Control" at the bottom of the popup

Name: "Xiaomi Dafang"

Type: "Fffmpeg"

Protocol: "Xiaomi" (it has to match the .pm file from above)

Can Reset: Yes

![pic](Screenshot%202018-04-30%2011.58.31.png)

### Move Tab

Can move: yes

Can move relative: yes

 ![pic](Screenshot%202018-04-30%2011.59.42.png)

### Pan Tab

Can pan: yes
 ![pic](Screenshot%202018-04-30%2012.00.13.png)

### Tilt Tab

Can tilt: yes
 ![pic](Screenshot%202018-04-30%2012.00.44.png)

That's it, now save your new control type and head back to the control tab

### Control Tab

Select "Controllable"

Control Type "Xiaomi Dafang"

Control Device: leave this empty

Control Address: root:ismart12@XX.XX.XX.XX (Where XX.XX.XX.XX is the IP of your camera)
![pic](Screenshot%202018-04-30%2012.02.19.png)
