#!/bin/sh
# Check if there is new parameters in the dist config file

CONF_PATH="/system/sdcard/config"
CONF_LIST="mqtt.conf rtspserver.conf matrix.conf motion.conf autonight.conf letsencrypt.conf sendmail.conf swap.conf telegram.conf"

# Print the variable names of a config file: "export NAME=" gives NAME; empty names and names with spaces are skipped
conf_keys()
{
    grep -o '^[^#]*' "$1" | cut -d= -f1 | awk '{ sub(/^export /, "") } $0 != "" && $0 !~ /[ \t]/' | sort
}

for CONF in $CONF_LIST; do
    CONF_NEW_VARS_COUNT=0
    if [ -f "${CONF_PATH}/${CONF}" ]; then
        echo "Check ${CONF}"
        CONF_DIST_VARS=$(conf_keys "${CONF_PATH}/${CONF}.dist")
        CONF_USER_VARS=$(conf_keys "${CONF_PATH}/${CONF}")
        for VAR in $CONF_DIST_VARS; do
            if ! printf '%s\n' "$CONF_USER_VARS" | grep -q "^${VAR}$"; then
                CONF_NEW_VARS_COUNT=$((CONF_NEW_VARS_COUNT+1))
                echo "# Parameter added by merge tool" >> "${CONF_PATH}/${CONF}"
                grep -m1 -E "^(export )?${VAR}=" "${CONF_PATH}/${CONF}.dist" >> "${CONF_PATH}/${CONF}"
            fi
        done
        if [ "$CONF_NEW_VARS_COUNT" -eq 0 ]; then
            echo "No new parameters between ${CONF} ${CONF}.dist"
        else
            echo "Merging ${CONF_NEW_VARS_COUNT} parameters in ${CONF}"
        fi
    else
      echo "${CONF} not exist"
    fi
done
