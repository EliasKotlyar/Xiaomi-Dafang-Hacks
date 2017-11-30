# Software


### JpegSnap
creates a JPEG from the Camera and outputs it to stdout

Usage:

./jpegSnap > image.jpg

## h264Snap 

Creates a h264 stream and outputs it to stdout

Usage:

./h264Snap > test.h264

(Cancel after some time)

## mJpegStreamer

Streams the Camera as mjpeg

Usage:

./mJpegStreamer


## h264Streamer

Streams a file which is passed via stdin

Usage
1. Download some example file from http://www.live555.com/liveMedia/public/264/
2. Stream it using cat <file> > ./h264streamer 

Attention: Dont try to combine it the the h264snap - it wont work. I tested it first. 

## Motor


1. Remove the old Module from Xiaomi: rmmod sample_motor
2. Insert the new Kernel Module : insmod ./sample_motor.ko
3. Run the Test-Application : ./motor

## Sample-Audio
Plays a wav file. Provide it as file.wav