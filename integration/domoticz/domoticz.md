## Xiaomi Dafang Integration in Domoticz

To control the camera in Domoticz one can create four virtual switches with a script action as on command.
Set a off delay at 1 sec
And as http:// script:

https://[web_login]:[web_password]@[ip_of_camera]/cgi-bin/action.cgi?cmd=motor_right

https://[web_login]:[web_password]@[ip_of_camera]/cgi-bin/action.cgi?cmd=motor_left

https://[web_login]:[web_password]@[ip_of_camera]/cgi-bin/action.cgi?cmd=motor_up

https://[web_login]:[web_password]@[ip_of_camera]/cgi-bin/action.cgi?cmd=motor_down

For more information please see the [original source](https://gadget-freakz.com/2018/03/xiaomi-1080p-xiaofang-camera-review/).

Another useful commands:

https://[web_login]:[web_password]@[ip_of_camera]/cgi-bin/action.cgi?cmd=showlog&logname=[""|(1-7)]

where logname="", or 1, or 2, ... or 7

https://[web_login]:[web_password]@[ip_of_camera]/cgi-bin/action.cgi?cmd=clearlog&logname=[""|(1-7)]

https://[web_login]:[web_password]@[ip_of_camera]/cgi-bin/action.cgi?cmd=reboot

https://[web_login]:[web_password]@[ip_of_camera]/cgi-bin/action.cgi?cmd=shutdown

https://[web_login]:[web_password]@[ip_of_camera]/cgi-bin/action.cgi?cmd=blue_led_on

https://[web_login]:[web_password]@[ip_of_camera]/cgi-bin/action.cgi?cmd=blue_led_off

https://[web_login]:[web_password]@[ip_of_camera]/cgi-bin/action.cgi?cmd=yellow_led_on

https://[web_login]:[web_password]@[ip_of_camera]/cgi-bin/action.cgi?cmd=yellow_led_off

https://[web_login]:[web_password]@[ip_of_camera]/cgi-bin/action.cgi?cmd=ir_led_on

https://[web_login]:[web_password]@[ip_of_camera]/cgi-bin/action.cgi?cmd=ir_led_off

https://[web_login]:[web_password]@[ip_of_camera]/cgi-bin/action.cgi?cmd=ir_cut_on

https://[web_login]:[web_password]@[ip_of_camera]/cgi-bin/action.cgi?cmd=ir_cut_off

https://[web_login]:[web_password]@[ip_of_camera]/cgi-bin/action.cgi?cmd=audio_test

https://[web_login]:[web_password]@[ip_of_camera]/cgi-bin/action.cgi?cmd=h264_start

https://[web_login]:[web_password]@[ip_of_camera]/cgi-bin/action.cgi?cmd=h264_noseg_start

https://[web_login]:[web_password]@[ip_of_camera]/cgi-bin/action.cgi?cmd=mjpeg_start

https://[web_login]:[web_password]@[ip_of_camera]/cgi-bin/action.cgi?cmd=h264_nosegmentation_start

https://[web_login]:[web_password]@[ip_of_camera]/cgi-bin/action.cgi?cmd=rtsp_stop

https://[web_login]:[web_password]@[ip_of_camera]/cgi-bin/action.cgi?cmd=set_http_password

https://[web_login]:[web_password]@[ip_of_camera]/cgi-bin/action.cgi?cmd=auto_night_mode_start

https://[web_login]:[web_password]@[ip_of_camera]/cgi-bin/action.cgi?cmd=auto_night_mode_stop

https://[web_login]:[web_password]@[ip_of_camera]/cgi-bin/action.cgi?cmd=toggle-rtsp-nightvision-on

https://[web_login]:[web_password]@[ip_of_camera]/cgi-bin/action.cgi?cmd=toggle-rtsp-nightvision-off

https://[web_login]:[web_password]@[ip_of_camera]/cgi-bin/action.cgi?cmd=flip-on

https://[web_login]:[web_password]@[ip_of_camera]/cgi-bin/action.cgi?cmd=flip-off

https://[web_login]:[web_password]@[ip_of_camera]/cgi-bin/action.cgi?cmd=motion_detection_on

https://[web_login]:[web_password]@[ip_of_camera]/cgi-bin/action.cgi?cmd=motion_detection_off

https://[web_login]:[web_password]@[ip_of_camera]/cgi-bin/action.cgi?cmd=autonight_sw

https://[web_login]:[web_password]@[ip_of_camera]/cgi-bin/action.cgi?cmd=autonight_hw

https://[web_login]:[web_password]@[ip_of_camera]/cgi-bin/action.cgi?cmd=offDebug

https://[web_login]:[web_password]@[ip_of_camera]/cgi-bin/action.cgi?cmd=onDebug

https://[web_login]:[web_password]@[ip_of_camera]/cgi-bin/action.cgi?cmd=update

https://[web_login]:[web_password]@[ip_of_camera]/cgi-bin/action.cgi?cmd=show_updateProgress

https://[web_login]:[web_password]@[ip_of_camera]/cgi-bin/action.cgi?cmd=motion_detection_mail_on

https://[web_login]:[web_password]@[ip_of_camera]/cgi-bin/action.cgi?cmd=motion_detection_mail_off

https://[web_login]:[web_password]@[ip_of_camera]/cgi-bin/action.cgi?cmd=motion_detection_telegram_on

https://[web_login]:[web_password]@[ip_of_camera]/cgi-bin/action.cgi?cmd=motion_detection_telegram_off

https://[web_login]:[web_password]@[ip_of_camera]/cgi-bin/action.cgi?cmd=motion_detection_led_on

https://[web_login]:[web_password]@[ip_of_camera]/cgi-bin/action.cgi?cmd=motion_detection_led_off

https://[web_login]:[web_password]@[ip_of_camera]/cgi-bin/action.cgi?cmd=motion_detection_snapshot_on

https://[web_login]:[web_password]@[ip_of_camera]/cgi-bin/action.cgi?cmd=motion_detection_snapshot_off

https://[web_login]:[web_password]@[ip_of_camera]/cgi-bin/action.cgi?cmd=motion_detection_mqtt_publish_on

https://[web_login]:[web_password]@[ip_of_camera]/cgi-bin/action.cgi?cmd=motion_detection_mqtt_publish_off

https://[web_login]:[web_password]@[ip_of_camera]/cgi-bin/action.cgi?cmd=motion_detection_mqtt_snapshot_on

https://[web_login]:[web_password]@[ip_of_camera]/cgi-bin/action.cgi?cmd=motion_detection_mqtt_snapshot_off
