#!/bin/sh
#
# Update the cacert, based on Mozilla CA certificate store
#
# The downloaded file is licensed under MPL 2.0
#
# We don't mind you downloading the PEM file from us in an automated fashion,
# but please don't do it more often than once per day. It is only updated once
# every few months anyway.
# ABOUT: https://curl.haxx.se/docs/caextract.html

curl --remote-name --time-cond cacert.pem https://curl.haxx.se/ca/cacert.pem
