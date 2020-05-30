#!/bin/sh

# This will be verbose, and issue a testing cert
# When it is successful, comment out the following line
# to issue a real cert. (LetsEncrypt limits the freq of
# real ones, so only comment out when it works.)
DEBUG="--test --debug"

CONFIGPATH="/system/sdcard/config"
ACMEPATH="${CONFIGPATH}/ssl/acme"

mkdir -p "${ACMEPATH}"

if [ ! -f "${CONFIGPATH}/letsencrypt.conf" ]; then
  echo "You must configure ${CONFIGPATH}/letsencrypt.conf before using letsencrypt_setup.sh"
  exit 1
fi

. $CONFIGPATH/letsencrypt.conf

if [ ! -d "acme.sh" ]; then
  echo "- Downloading the acme.sh script..."
  wget -q https://github.com/acmesh-official/acme.sh/archive/master.zip
  unzip -q master.zip
  mv acme.sh-master acme.sh
  rm master.zip
fi

if [ -d "${ACMEPATH}/${LETSENCRYPT_DOMAIN}" ]; then
  echo "ERROR: It seems this process has already been done, you might want to delete:"
  echo " - $ rm -r ${ACMEPATH}/"
  exit 1
fi

export OPENSSL_CONF="${CONFIGPATH}/openssl.cnf"
if [ "$LETSENCRYPT_METHOD" = "webroot" ]; then
	./acme.sh/acme.sh --issue -d ${LETSENCRYPT_DOMAIN} --home ${ACMEPATH} \
	  -w ${CONFIGPATH}/../www/ \
	  ${DEBUG}
elif [ "$LETSENCRYPT_METHOD" = "dns" ]; then
	./acme.sh/acme.sh --issue -d ${LETSENCRYPT_DOMAIN} --home ${ACMEPATH} \
	  --dns ${LETSENCRYPT_DNS_PROVIDER} \
	  ${DEBUG}
fi

./acme.sh/acme.sh --install-cert -d ${LETSENCRYPT_DOMAIN} --home ${ACMEPATH} \
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

$(pwd)/acme.sh/acme.sh --cron --home ${ACMEPATH} >> /tmp/letsencrypt_cron.log 2>&1
EOF

if [ ! -z "${DEBUG}" ]; then
  echo "** If it all looks good, remove the DEBUG at the top of the script to generate real certs!! **"
fi
