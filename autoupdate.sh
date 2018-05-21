#!/bin/sh
##########################################################################
# Github autodownload script
# See usage for help
# Edit the global variables to change the repo and initial folder
# Depends on curl, jq (jason paser), openssl (SHA calculation)

# owner name and repo name
REPO="EliasKotlyar/Xiaomi-Dafang-Hacks"
# Branch to use
BRANCH="master"
# Initial remote folder
REMOTEFOLDER="firmware_mod"
# Default destination foler
DESTFOLDER="./"
DESTOVERRIDE="/tmp/Update"
# The list of exclude, can have multple filter with "*.conf|*.sh"
EXCLUDEFILTER=""
#"*.conf|*.user|run.sh|osd|autoupdate.sh|libcrypto.so.42|curl|curl.bin|libssl.so.44|libz.so.1"
# Somme URL
GITHUBURL="https://api.github.com/repos"
GITHUBURLRAW="https://raw.githubusercontent.com"
CURL="curl -k"
JQ="jq"
SHA="openssl dgst -sha256"
BASENAME="basename"
#CURL="/system/sdcard/bin/curl -k"
#JQ="/system/sdcard/bin/jq"
#SHA="/system/sdcard/bin/openssl dgst -sha256"
#BASENAME="/system/sdcard/bin/busybox basename"

TMPFILE=/tmp/udpate.tmp
BACKUPEXT=.backup
LASTGLOBALCOMMIT=""
_PRINTONLY=0
_V=0
_FORCE=0
_XFER=1
_BACKUP=0
##########################################################################

usage()
{
    echo "Usage: $1 [OPTIONS]"
    echo "$1 will update a local folder with the ${REPO} github repo (first copy all the files in ${DESTOVERRIDE}, stop services and reboot"
    echo "Usage this script to update the ${REPO} github repo from ${BRANCH} branch"
    echo "Options:"
    echo "-b (--backup) backup erased file (add extension ${BACKUPEXT} to the local file before ovewrite it) "
    echo "-f (--force) force update"
    echo "-d (--dest) set the destination folder (default is ${DESTFOLDER})"
    echo "-p (--print) print action only, do nothing"

    echo "-v (--verbose) for verbose"
    echo "-u (--user) githup login/password (not mandatory, but sometime anonymous account get banned)"
    echo "-h (--help) for this help"
    echo 
    echo "Note that ${EXCLUDEFILTER} will be excluded"
    echo "Examples:"
    echo "Update all files if needed >$1 -d /system/sdcard (-f to force update)"
}

##########################################################################
# Function to get user input for yes/no/all
# print the result (yes,no,all)
ask_yes_or_no() {
    read R
    case $(echo ${R} | tr '[A-Z]' '[a-z]') in
        y|yes) echo "yes" ;;
    a|all) echo "all" ;;
*)     echo "no" ;;
  esac
}

##########################################################################
# Log string if verbose is set
log ()
{
    if [ ${_V} -eq 1 ]; then
        echo "$@"
    fi
}

##########################################################################
# Log string on std error
logerror ()
{
    echo "$@" 1>&2
}

##########################################################################
# If "printonly" action is selected print the action to do (but don't do it
# If not execute it
action()
{
    if [ ${_PRINTONLY} -eq 1 ]; then
        echo "Action: $@"
    else
        eval "$@"
    fi
    return $?
}
##########################################################################
# Check if $1 macth with the excluded filter
ismatch()
{
    in=$(${BASENAME} ${1})
    echo notmatch
    return 0
    for filter in $(echo ${EXCLUDEFILTER} | sed "s/|/ /g")
    do
        if [ "${in#$filter}" == "" ]; then
            echo match
            return 0
        fi
    done

    echo notmatch
}

##########################################################################
# Return the current (last) commit from the specified repo and branch
getCurrentCommitFromRemote()
{
    CURRENTCOMMIT=$(${CURL} -s ${GITHUBURL}/${REPO}/commits/${BRANCH} | grep sha | head -1 | cut -d'"' -f 4)
    #CURRENTCOMMIT=$(curl -s https://github.com/${REPO}/commits/${BRANCH} 2>/dev/null| grep "commit:" | head -1| cut -d ":" -f 4 |sed 's/"//')
    echo ${CURRENTCOMMIT}
}

##########################################################################
# Print the files from repo of the folder $1
# Recursive call (for folder)
getfiles()
{
    if echo "${1}" | grep -q "API rate limit exceeded"; then
        logerror "Github limit exceeded, try with an account (-u option)"
        exit 1
    else
        for row in $(echo "${1}" | ${JQ} '.[]| select(.type=="file") | .download_url' ); do
            filetoget=$(echo "${row}" | tr -d '"')
            echo ${filetoget}
        done

        for row in $(echo "${1}" | ${JQ} '.[]| select(.type == "dir") | .path' ); do
            flder=$(echo "${row}" | tr -d '"')
            next=$(${CURL} -s https://api.github.com/repos/${REPO}/contents/${flder}?ref=${BRANCH})
            getfiles "${next}"
        done
    fi
}

##########################################################################
# Script real start

while [ $# -gt 0 ]
do
    arg="$1"
    case ${arg} in
        "")
            ;;
        -v | --verbose)
            _V=1
            shift
            ;;
        -f | --force)
            _FORCE=1
            shift
            ;;
        -d | --dest)
            DESTFOLDER="$2/"
            shift
            shift
            ;;
        -b | --backup)
            _BACKUP=1;
            shift
            ;;
        -p | --print)
            _PRINTONLY=1
            shift
            ;;
        -u | --user)
            CURL="${CURL} -u $2"
            shift
            shift
            ;;
        *|-h |\? | --help)
            usage $0
            exit 1
            ;;
    esac
done

log "Start"

if [ ${_FORCE} = 1 ]; then
    log "Forced update"
else
    log "Need to be updated = ${update}"
fi

if [ ${_XFER} = 1 ]; then
    log "Transfert and check file by file"
    # Force update
    update=true
fi

if [ ${_FORCE} = 1 ]; then
    log "forced option"
fi

if [ ${_PRINTONLY} = 1 ]; then
    log "Print actions only, do nothing"
fi

if [ ${_BACKUP} = 1 ]; then
  log "will backup files"
fi

action "rm -rf ${DESTOVERRIDE} 2>/dev/null"

log "Get list of files"
FIRST=$(${CURL} -s ${GITHUBURL}/${REPO}/contents/${REMOTEFOLDER}?ref=${BRANCH})
FILES=$(getfiles "${FIRST}")
# For all the repository files
for i in ${FILES}
do
    # String to remove to get the local path
    REMOVE="${GITHUBURLRAW}/${REPO}/${BRANCH}/${REMOTEFOLDER}/"
    LOCALFILE="${DESTFOLDER}${i#$REMOVE}"
    # Remove files that match the filter
    res=$(ismatch ${LOCALFILE})
    #if [ "$res" == "match" ]; then
    #    echo "${LOCALFILE} is excluded due to filter"
    #    continue
    #fi
    # If ask to xfer for all
    if [  ${_XFER} = 1 ] ; then
        # Get the file temporally to calculate SHA
        ${CURL} -s ${i} -o ${TMPFILE} 2>/dev/null
        if [ ! -f ${TMPFILE} ]; then
            echo "Can not get remote file $i, exit"
            exit 1
        fi

        # Check the file exists in local
        if [ -f "${LOCALFILE}" ]; then
            REMOTESHA=$(${SHA} ${TMPFILE} 2>/dev/null | cut -d "=" -f 2)
            # Calculate the remote and local SHA
            LOCALSHA=$(${SHA} ${LOCALFILE} 2>/dev/null | cut -d "=" -f 2)

            # log "SHA of $LOCALFILE is ${LOCALSHA} ** remote is ${REMOTESHA}"
            if [ "${REMOTESHA}" = "${LOCALSHA}" ] ; then
                echo "${LOCALFILE} is OK"
            else
                if [ ${_XFER} = 1 ]; then
                    if [ ${_FORCE} = 1 ]; then
                        echo "${LOCALFILE} updated"
                        action "mkdir -p $(dirname ${DESTOVERRIDE}/${LOCALFILE}) 2>/dev/null"
                        if [ ${_BACKUP} = 1 ]; then
                            action cp ${LOCALFILE} ${DESTOVERRIDE}/${LOCALFILE}${BACKUPEXT}
                        fi
                        action mv ${TMPFILE} ${DESTOVERRIDE}/${LOCALFILE}
                    else
                        echo "${LOCALFILE} need to be updated, overwrite [Y]es or [N]o or [A]ll ?"
                        rep=$(ask_yes_or_no )
                        if [ "${rep}" = "no" ]; then
                            echo "${LOCALFILE} not updated"
                            rm -f ${TMPFILE} 2>/dev/null
                        else
                            action "mkdir -p $(dirname ${DESTOVERRIDE}/${LOCALFILE}) 2>/dev/null"
                            if [ ${_BACKUP} = 1 ]; then
                                action cp ${LOCALFILE} ${DESTOVERRIDE}/${LOCALFILE}${BACKUPEXT}
                            fi
                            action mv ${TMPFILE} ${DESTOVERRIDE}/${LOCALFILE}

                        fi
                        if [ "${rep}" = "all" ]; then
                            _FORCE=1
                        fi
                    fi
                else
                    echo "${LOCALFILE} is different from repo"
                fi
            fi
        else
            if [ ${_XFER} = 1 ]; then
                if [ ${_FORCE} = 1 ]; then
                    echo "${LOCALFILE} created"
                    action "mkdir -p $(dirname ${DESTOVERRIDE}/${LOCALFILE}) 2>/dev/null"
                    action mv ${TMPFILE} ${DESTOVERRIDE}/${LOCALFILE}
                else
                    echo "${LOCALFILE} doesn't exist, create it [Y]es or [N]o or [A]ll ?"
                    rep=$(ask_yes_or_no )
                    if [ "${rep}" = "no" ]; then
                        echo "${LOCALFILE} not created"
                        rm -f ${TMPFILE} 2>/dev/null
                    else  
                        action "mkdir -p $(dirname ${DESTOVERRIDE}/${LOCALFILE}) 2>/dev/null"
                        action mv ${TMPFILE} ${DESTOVERRIDE}/${LOCALFILE}
                    fi
                    if [ "${rep}" = "all" ]; then
                        _FORCE=1
                    fi
                fi
            else
                echo "${LOCALFILE} is missing"
            fi
        fi
    else
        log "Get ${i}"
        action ${CURL} -s ${i} --create-dirs -o ${LOCALFILE}
        if [ $? -ne 0 ]; then
            logerror "Failed to get ${LOCALFILE}"
        fi
    fi


done
if [ -d ${DESTOVERRIDE} ] && [ $(ls -l ${DESTOVERRIDE}/* | wc -l 2>/dev/null) > 1 ]; then
    echo "--------------- Stop services ---------"

    echo "--------------- Update files ----------"
    action "cp -Rf ${DESTOVERRIDE}/* ${DESTFOLDER} 2>/dev/null"
    action "rm -Rf ${DESTOVERRIDE}/* 2>/dev/null"

    echo "---------------    Reboot    ----------"
    action echo reboot
else
    echo "No updated files, no actions"
fi
