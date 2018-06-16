#!/bin/sh

# This will be verbose, and issue a testing cert
# When it is successful, comment out the following line
# to issue a real cert. (LetsEncrypt limits the freq of
# real ones, so only comment out when it works.)
DEBUG="--test --debug"

CONFIGPATH="/system/sdcard/config"
ACMEPATH="${CONFIGPATH}/ssl/acme"
SSL_DOMAIN_PATH="${CONFIGPATH}/ssl_domain.conf"

if [ ! -f "acme.sh" ]; then
  echo "- Downloading the acme.sh script..."
  curl -s https://raw.githubusercontent.com/Neilpang/acme.sh/master/acme.sh > acme.sh
fi

if [ ! -f "${SSL_DOMAIN_PATH}" ]; then
   echo "ERROR: Please set domain name in file: ${SSL_DOMAIN_PATH}"
   echo "  ie, echo 'cam.example.org' > ${SSL_DOMAIN_PATH}"
   exit 1
fi

SSL_DOMAIN=$(cat ${SSL_DOMAIN_PATH})
export OPENSSL_CONF="${CONFIGPATH}/openssl.cnf"

if [ -d "${ACMEPATH}/${SSL_DOMAIN}" ]; then
  echo "ERROR: It seems this process has already been done, you might want to delete:"
  echo " - $ rm -r ${ACMEPATH}/"
  exit 1
fi

./acme.sh --issue -d ${SSL_DOMAIN} --home ${ACMEPATH} \
          -w ${CONFIGPATH}/../www/ \
          ${DEBUG}

./acme.sh --install-cert -d ${SSL_DOMAIN} --home ${ACMEPATH} \
          --cert-file ${ACMEPATH}/host.crt \
          --key-file  ${ACMEPATH}/host.key \
          --fullchain-file ${ACMEPATH}/fullchain.crt \
          --reloadcmd  "cat ${ACMEPATH}/host.crt ${ACMEPATH}/host.key > ${CONFIGPATH}/lighttpd.pem ;\
                        pkill lighttpd.bin ;\
                        /system/sdcard/bin/lighttpd -f ${CONFIGPATH}/lighttpd.conf"


## Adding cronjob to keep the cert updated
cat > ${CONFIGPATH}/cron/periodic/weekly/letsencrypt <<EOF
#!/bin/sh
PATH=/system/sdcard/bin:/system/bin:/bin:/sbin:/usr/bin:/usr/sbin
CONFIGPATH="/system/sdcard/config"
export OPENSSL_CONF="${CONFIGPATH}/openssl.cnf"

$(pwd)/acme.sh --cron --home ${ACMEPATH} >> /tmp/letsencrypt_cron.log 2>&1
EOF

if [ ! -z "${DEBUG}" ]; then
  echo "** If it all looks good, remove the DEBUG at the top of the script to generate real certs!! **"
fi
