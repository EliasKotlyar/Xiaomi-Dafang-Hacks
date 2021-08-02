#!/bin/sh
what="$1"
shift
data="$@"
CURL="/system/sdcard/bin/curl"

. /system/sdcard/config/telegram.conf

sendMessage() {
  text="$(echo "${@}" | sed 's:\\n:\n:g')"
  echo "Sending message: $text"

  $CURL -s \
    -X POST \
    https://api.telegram.org/bot$apiToken/sendMessage \
    --data-urlencode "text=$text" \
    -d "chat_id=$userChatId"
}

sendFile() {
  if [ -r $1 ]
  then 
    echo "Sending file: $1"
    $CURL -s \
      -X POST \
      https://api.telegram.org/bot$apiToken/sendDocument \
      -F chat_id="$userChatId" \
      -F document=@"$1"
  else
    echo "File not found: $1"
  fi
}

sendPhoto() {
  if [ -r $1 ]
  then
    caption="$(hostname)-$(date +"%d%m%Y_%H%M%S")"
    echo "Sending Photo: $1 $caption" >> /tmp/telegram.log
    $CURL -s \
      -X POST \
      https://api.telegram.org/bot$apiToken/sendPhoto \
      -F chat_id="$userChatId" \
      -F photo="@${1}" \
      -F caption="${caption}"
  else
    echo "File not found: $1"
  fi
}

sendVideo() {
  if [ -r $1 ]
  then
    bytes=$(busybox stat -c %s $1)
    caption="$(hostname)-$(date +"%d%m%Y_%H%M%S")"
    echo "Sending Video: $1 $caption (${bytes}bytes)" >> /tmp/telegram.log
    $CURL -s \
      -X POST \
      https://api.telegram.org/bot$apiToken/sendVideo \
      -F chat_id="$userChatId" \
      -F video="@${1}" \
      -F caption="${caption}"
  else
    echo "File not found: $1"
  fi
}

sendAnimation() {
  if [ -r $1 ]
  then
    caption="$(hostname)-$(date +"%d%m%Y_%H%M%S")"
    echo "Sending Animation: $1 $caption" >> /tmp/telegram.log
    $CURL -s \
      -X POST \
      https://api.telegram.org/bot$apiToken/sendAnimation \
      -F chat_id="$userChatId" \
      -F animation="@${1}" \
      -F caption="${caption}"
  else
    echo "File not found: $1"
  fi
}

[ "$what" == "m" ] && sendMessage $data
[ "$what" == "f" ] && sendFile $data
[ "$what" == "p" ] && sendPhoto $data
[ "$what" == "v" ] && sendVideo $data
[ "$what" == "a" ] && sendAnimation $data

[ -z "$what" ] && echo -e "$0 <m|f|p> <data>\n m: message\n f: file\n p: picture\n v: video\n a: animation"
