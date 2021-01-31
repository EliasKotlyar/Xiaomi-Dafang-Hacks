#!/bin/sh

 . /system/sdcard/scripts/common_functions.sh

LOGDIR="/system/sdcard/log"
LOGPATH="$LOGDIR/telegram.log"
if [ ! -d $LOGDIR ]; then
  mkdir -p $LOGDIR
fi




CURL="/system/sdcard/bin/curl"
LASTUPDATEFILE="/tmp/last_update_id"
JQ="/system/sdcard/bin/jq"

. /system/sdcard/config/telegram.conf
[ -z $apiToken ] && echo "api token not configured yet" && exit 1
[ -z $userChatId ] && echo "chat id not configured yet" && exit 1

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
  echo "Sending file: $1"
  $CURL -s \
    -X POST \
    https://api.telegram.org/bot$apiToken/sendDocument \
    -F chat_id="$userChatId" \
    -F document=@"$1"
}

sendPhoto() {
  caption="$(hostname)-$(date +"%d%m%Y_%H%M%S")"
  echo "Sending Photo: $1 $caption" >> $LOGPATH
  $CURL -s \
    -X POST \
    https://api.telegram.org/bot$apiToken/sendPhoto \
    -F chat_id="$userChatId" \
    -F photo="@${1}" \
    -F caption="${caption}"
}

sendVideo() {
  caption="$(hostname)-$(date +"%d%m%Y_%H%M%S")"
  echo "Sending Video: $1 $caption" >> $LOGPATH
  $CURL -s \
    -X POST \
    https://api.telegram.org/bot$apiToken/sendVideo \
    -F chat_id="$userChatId" \
    -F video="@${1}" \
    -F caption="${caption}"
}

sendAnimation() {
  caption="$(hostname)-$(date +"%d%m%Y_%H%M%S")"
  echo "Sending Animation: $1 $caption" >> $LOGPATH
  $CURL -s \
    -X POST \
    https://api.telegram.org/bot$apiToken/sendAnimation \
    -F chat_id="$userChatId" \
    -F animation="@${1}" \
    -F caption="${caption}"
}

sendShot() {
  /system/sdcard/bin/getimage > "/tmp/telegram_image.jpg" &&\
  sendPhoto "/tmp/telegram_image.jpg"
  rm "/tmp/telegram_image.jpg"
}






sendMem() {
  sendMessage $(free -k | awk '/^Mem/ {print "Mem: used "$3" free "$4} /^Swap/ {print "Swap: used "$3}')  
}

nightOn() {
  night_mode on && sendMessage "Night mode active"
}

nightOff() {
  night_mode off && sendMessage "Night mode inactive"
}

detectionOn() {
  motion_detection on && sendMessage "Motion detection started"
}

detectionOff() {
  motion_detection off && sendMessage "Motion detection stopped"
}

textAlerts() {
  rewrite_config /system/sdcard/config/motion.conf telegram_alert_type "text"
  sendMessage "Text alerts on motion detection enabled"
}

imageAlerts() {
  rewrite_config /system/sdcard/config/motion.conf telegram_alert_type "image"
  sendMessage "Image alerts on motion detection enabled"
}

videoAlerts() {
  rewrite_config /system/sdcard/config/motion.conf telegram_alert_type "video"
  sendMessage "Video alerts on motion detection enabled"
}

respond() {
  cmd=$1
  echo "Responding to command: $cmd" >> $LOGPATH
  [ $chatId -lt 0 ] && cmd=${1%%@*}
  case $cmd in
	/mem) sendMem;;
	/shot) sendShot;;
	/on) detectionOn;;
	/off) detectionOff;;
	/nighton) nightOn;;
	/nightoff) nightOff;;
	/textalerts) textAlerts;;
	/imagealerts) imageAlerts;;
	/videoalerts) videoAlerts;;
	/help | /start) sendMessage "######### Bot commands #########\n# /mem - show memory information\n# /shot - take a snapshot\n# /on - motion detection on\n# /off - motion detection off\n# /nighton - night mode on\n# /nightoff - night mode off\n# /textalerts - Text alerts on motion detection\n# /imagealerts - Image alerts on motion detection\n# /videoalerts - Video alerts on motion detection";;
	*) sendMessage "I can't respond to '$cmd' command"
  esac
  #echo "Telegram Daemon Responded" >> $LOGPATH
}

readNext() {
  lastUpdateId=$(cat $LASTUPDATEFILE || echo "0")
  json=$($CURL -s -X GET "https://api.telegram.org/bot$apiToken/getUpdates?offset=$lastUpdateId&limit=1&allowed_updates=message")
  echo $json
}

markAsRead() {
  nextId=$(($1 + 1))
  echo "$nextId" > $LASTUPDATEFILE
}

main() {
  #echo "\r\nTelegram starting MAIN" >> $LOGPATH

  json=$(readNext)

  #echo "Received from Telegram: $json" >> $LOGPATH

  [ -z "$json" ] && return 0
  if [ "$(echo "$json" | $JQ -r '.ok')" != "true" ]; then
	echo "$(date '+%F %T') Bot error: $json" >> $LOGPATH
	[ "$(echo "$json" | $JQ -r '.error_code')" == "401" ] && return 1
	return 0
  fi;

  messageAttr="message"
  messageVal=$(echo "$json" | $JQ -r '.result[0].message // ""')
  [ -z "$messageVal" ] && messageAttr="edited_message" && messageVal=$(echo "$json" | $JQ -r '.result[0].edited_message // ""')
  [ -z "$messageVal" ] && messageAttr="channel_post"
  chatId=$(echo "$json" | $JQ -r ".result[0].$messageAttr.chat.id // \"\"")
  updateId=$(echo "$json" | $JQ -r '.result[0].update_id // ""')

  #echo "messageAttr: $messageAttr" >> $LOGPATH
  #echo "messageVal: $messageVal" >> $LOGPATH
  #echo "chatId: $chatId" >> $LOGPATH
  #echo "updateId: $updateId" >> $LOGPATH
  #echo "userChatId: $userChatId" >> $LOGPATH

  if [ "$updateId" != "" ] && [ -z "$chatId" ]; then
  markAsRead $updateId
  return 0
  fi;

  [ -z "$chatId" ] && return 0 # no new messages

  cmd=$(echo "$json" | $JQ -r ".result[0].$messageAttr.text // \"\"")

  #echo "cmd: $cmd" >> $LOGPATH

  if [ "$chatId" != "$userChatId" ]; then
	username=$(echo "$json" | $JQ -r ".result[0].$messageAttr.from.username // \"\"")
	firstName=$(echo "$json" | $JQ -r ".result[0].$messageAttr.from.first_name // \"\"")
	sendMessage "Received message from unauthorized chat id: $chatId\nUser: $username($firstName)\nMessage: $cmd"
  else
	respond $cmd
  fi;

  markAsRead $updateId

  #echo "Marked $updateId as read." >> $LOGPATH
}

while true; do
  main >/dev/null 2>&1
  [ $? -gt 0 ] && exit 1
  sleep 2
done;
