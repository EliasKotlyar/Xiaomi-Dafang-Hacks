#!/bin/sh
user=$1
# realm is defined in the lightppd.conf
realm="all"
pass=$2
hash=$(echo -n "$user:$realm:$pass" | md5sum | cut -b -32)
echo "$user:$realm:$hash"
