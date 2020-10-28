#!/bin/sh
# Check if there is new parameters in the dist config file

CONF_PATH="/system/sdcard/config"
CONF_LIST="mqtt.conf rtspserver.conf matrix.conf motion.conf autonight.conf letsencrypt.conf sendmail.conf swap.conf telegram.conf"

for CONF in $CONF_LIST; do
    CONF_NEW_VARS_COUNT=0
    if [ -f "${CONF_PATH}/${CONF}" ]; then
        echo "Check ${CONF}"
        CONF_DIST_VARS=$(grep -o '^[^#]*' "${CONF_PATH}/${CONF}.dist" | cut -d= -f1 | sort)
        CONF_USER_VARS=$(grep -o '^[^#]*' ${CONF_PATH}/${CONF} | cut -d= -f1 | sort)
        for VAR in $CONF_DIST_VARS; do
            if [ ! -n  "$(echo $CONF_USER_VARS | grep $VAR)" ]; then
                CONF_NEW_VARS_COUNT=$((CONF_NEW_VARS_COUNT+1))
                echo "# Parameter added by merge tool" >> "${CONF_PATH}/${CONF}"
                grep $VAR "${CONF_PATH}/${CONF}.dist" >> "${CONF_PATH}/${CONF}"
            fi
        done
        if [ $CONF_NEW_VARS_COUNT == 0 ]; then
            echo "No new parameters between ${CONF} ${CONF}.dist"
        else
            echo "Merging ${CONF_NEW_VARS_COUNT} parameters in ${CONF}"
        fi
    else
      echo "${CONF} not exist"
    fi
done