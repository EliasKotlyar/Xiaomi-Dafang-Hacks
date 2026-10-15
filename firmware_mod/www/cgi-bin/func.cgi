#!/bin/sh
# Source: http://isquared.nl/blog/2008/11/01/Bourne-Bash-Shell-CGI-Scripts/

_DEBUG_=

if [ "${REQUEST_METHOD}" = "POST" ]
then
  POST_QUERY_STRING=`dd bs=1 count=${CONTENT_LENGTH} 2>/dev/null`
  if [ "${QUERY_STRING}" != "" ]
  then
      QUERY_STRING=${POST_QUERY_STRING}"&"${QUERY_STRING}
  else
      QUERY_STRING=${POST_QUERY_STRING}"&"
  fi
fi

#echo "Content-type: text/plain"; echo

_IFS=${IFS}; IFS=\&
set -f
i=0
for _VAR in ${QUERY_STRING}
do
  if [ ${_DEBUG_} ]
  then
      i=`expr $i + 1`; echo "--- ENTER LOOP $i ---"
      echo _VAR: ${_VAR}
      echo -n variable: `echo ${_VAR} | cut -d= -f1`" "
      echo value: `echo ${_VAR} | cut -d= -f2`
  fi

  _KEY=${_VAR%%=*}
  _VALUE=${_VAR#*=}
  case "${_KEY}" in
    ''|*[!A-Za-z0-9_]* )
      continue
      ;;
  esac
  export "F_${_KEY}=${_VALUE}"

  if [ ${_DEBUG_} ]
  then
      echo "--- EXIT LOOP $i ---"
  fi
done
set +f
IFS=${_IFS}
unset i _IFS _VAR _KEY _VALUE

if [ ${_DEBUG_} ]
then
  echo query string: ${QUERY_STRING}
  echo post-part of query string: ${POST_QUERY_STRING}
fi
