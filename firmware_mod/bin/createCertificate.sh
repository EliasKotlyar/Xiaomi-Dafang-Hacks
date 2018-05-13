#!/bin/sh

CreateCertificateAuthority() {

if [ -f ./ubntCA.key ]; then rm ./ubntCA.key; fi
if [ -f ./ubntCA.pem ]; then rm ./ubntCA.pem; fi

#
# Create the Root Key
#
/system/sdcard/bin/openssl genrsa -out ubntCA.key 2048

#
# Now self-sign this certificate using the root key.
#
# CN: CommonName
# OU: OrganizationalUnit
# O: Organization
# L: Locality
# S: StateOrProvinceName
# C: CountryName
#
/system/sdcard/bin/openssl req -x509 \
            -new \
            -nodes \
            -key ubntCA.key \
            -sha256 \
            -days 3650 \
            -subj "/C=US/ST=IS/L=TOTALLY/O=CONFUSED/OU=HERE/CN=THEKEYMASTER.COM" \
            -out ubntCA.pem

}

CreateServerCertificate() {

if [ -f ./server.key ]; then rm ./server.key; fi
if [ -f ./server.csr ]; then rm ./server.csr; fi
if [ -f ./server.crt ]; then rm ./server.crt; fi

#
# Create A Certificate
#
/system/sdcard/bin/openssl genrsa -out server.key 2048

#
# Now generate the certificate signing request.
#
/system/sdcard/bin/openssl req -new \
            -key server.key \
            -subj "/C=US/ST=IS/L=ALSOTOTALLY/O=CONFUSED/OU=HERE/CN=$1" \
            -out server.csr

#
# Now generate the final certificate from the signing request.
#
echo subjectAltName=DNS:$1 > tmp.file
/system/sdcard/bin/openssl x509 -req \
             -in server.csr \
             -CA ubntCA.pem \
             -CAkey ubntCA.key \
             -CAcreateserial \
             -extfile tmp.file \
             -out server.crt -days 3650 -sha256
rm -f tmp.file
}

CreateServerPem() {

cat server.crt  > server.pem
cat server.key >> server.pem

}
   if [  $# -eq 0 ] ; then
    echo "Usage $0 domain"
   else
       mkdir /tmp/tmp
       cd /tmp/tmp
       export OPENSSL_CONF=/system/sdcard/config/openssl.cnf
       CreateCertificateAuthority
       CreateServerCertificate $1
       CreateServerPem
       cp server.pem /system/sdcard/config/lighttpd.pem
       cp server.key /system/sdcard/config/lighttpd.key
       cp server.crt /system/sdcard/config/lighttpd.crt
       cp ubntCA.pem /system/sdcard/config/
       echo "Keys have been installed, restart lighttpd and audioserver, install /system/sdcard/config/lighttpd.pem and /system/sdcard/config/ubntCA.pem on Chrome/Firefox/..."
  fi
