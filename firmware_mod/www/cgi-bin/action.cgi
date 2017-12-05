#!/bin/sh

echo "Content-type: text/html"
echo ""

source func.cgi

setgpio(){
GPIOPIN=$1
echo $2 > /sys/class/gpio/gpio$GPIOPIN/value
}

echo "<br/>"
if [ -n "$F_cmd" ]; then
  case "$F_cmd" in
  showlog)
    echo "Contents of /tmp/hacks.log:<br/>"
    echo "<pre>"
    cat /tmp/hacks.log
    echo "</pre>"
    ;;
  reboot)
    echo "Rebooting device...<br/>"
    /sbin/reboot
    ;;
  blue_led_on)
    setgpio 39 1
    ;;
  blue_led_off)
    setgpio 39 0
    ;;
  *)
    echo "Unsupported command '$F_cmd'"
    ;;
  esac
fi

echo "<hr/>"
echo "<button title='Return to status page' onClick=\"window.location.href='status'\">Back</button>"
