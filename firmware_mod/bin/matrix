#!/bin/sh

CURL="/system/sdcard/bin/curl --silent"
JQ="/system/sdcard/bin/jq"

what="$1"

if [ "$what" = "m" ]; then
  shift
  sendtext="${@//\"/\\\"}"
else
  filename="$2"
  datafile="$3"
fi

. /system/sdcard/config/matrix.conf

uploadData() {
  mimetype="$1"
  msgtype="$2"

  mxcuri="$($CURL -XPOST -H "Content-Type: $mimetype" --data-binary @"$datafile" "https://$host:$port/_matrix/media/r0/upload?filename=$filename&access_token=$access_token" | $JQ -cMr ".content_uri")"
  if [ -n "$mxcuri" ] && [ "$mxcuri" != "null" ]; then
    $CURL -XPOST -d '{"msgtype":"'"$msgtype"'", "body":"'"$filename"'", "url":"'"$mxcuri"'"}' "https://$host:$port/_matrix/client/r0/rooms/$room_id/send/m.room.message?access_token=$access_token"
  fi
}

sendFile() {
  echo "Sending file: $datafile"
  uploadData "application/octet-stream" "m.file"
}

sendMessage() {
  echo "Sending message: $sendtext"
  $CURL -XPOST -d '{"msgtype":"m.notice", "body":"'"$sendtext"'"}' "https://$host:$port/_matrix/client/r0/rooms/$room_id/send/m.room.message?access_token=$access_token"
}

sendPicture() {
  echo "Sending picture: $datafile"
  filename="$filename.jpg"
  uploadData "image/jpeg" "m.image"
}

sendVideo() {
  echo "Sending video: $datafile"
  filename="$filename.mp4"
  uploadData "video/mp4" "m.video"
}

[ "$what" = "f" ] && sendFile
[ "$what" = "m" ] && sendMessage
[ "$what" = "p" ] && sendPicture
[ "$what" = "v" ] && sendVideo
[ -z "$what" ] && echo -e "$0 <m|f|p|v> <data|filename>\n m: message\n f: file\n p: picture\n v: video"
