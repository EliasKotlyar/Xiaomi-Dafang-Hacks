#!/bin/sh
##########################################################################
# Github autodownload script
# See usage for help
# Edit the global variables to change the repo and initial folder
# Depends on curl, jq (json parser), openssl (SHA calculation)

# owner name and repo name
REPO="EliasKotlyar/Xiaomi-Dafang-Hacks"
# Branch to use
BRANCH="master"
# Initial remote folder
REMOTEFOLDER="firmware_mod"
# Default destination foler
DESTFOLDER="/system/sdcard/"
DESTOVERRIDE="/tmp/Update"
# The list of exclude, can have multple filter with "*.conf|*.sh"
EXCLUDEFILTER="*.conf|*.user|passwd|shadow"
GITHUBURL="https://api.github.com/repos"
GITHUBURLRAW="https://raw.githubusercontent.com"
CURL="/system/sdcard/bin/curl -k -L"
JQ="/system/sdcard/bin/jq"
SHA="/system/sdcard/bin/openssl dgst -sha256"
BASENAME="/system/sdcard/bin/busybox basename"
FIND="/system/sdcard/bin/busybox find"
VERSION_FILE='/system/sdcard/VERSION'
COMMITS_FILE='/tmp/.lastcommit'



TMPFILE=/tmp/update.tmp
BACKUPEXT=.backup
_PRINTONLY=0
_V=0
_FORCE=0
_FORCEREBOOT=0
_BACKUP=0

_PROGRESS=0
_NBFILES=0
_NBTOTALFILES=0
##########################################################################

usage()
{
    echo "Usage: $1 [OPTIONS]"
    echo "$1 will update a local folder with the ${REPO} github repo (first copy all the files in ${DESTOVERRIDE}, stop services and reboot"
    echo "Usage this script to update the ${REPO} github repo from ${BRANCH} (default) branch"
    echo "Options:"
    echo "-b (--backup) backup erased file (add extension ${BACKUPEXT} to the local file before ovewrite it) "
    echo "-r (--branch) to set the branch"
    echo "-f (--force) force update"
    echo "-d (--dest) set the destination folder (default is ${DESTFOLDER})"
    echo "-p (--print) print action only, do nothing"
    echo "-s (--steps) add progress in file /tmp/progress"

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
# Log string on std error
progress()
{
        if [ ${_PROGRESS} -eq 1 ]; then
           _NBFILES=$((${_NBFILES} + 1))
           echo -n $((${_NBFILES} *100 / ${_NBTOTALFILES} )) > /tmp/progress
#      echo "file = ${_NBFILES}, total=${_NBTOTALFILES} = $((${_NBFILES} *100 / ${_NBTOTALFILES} ))"
        fi
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
# Let some time before rebooting
countdownreboot()
{
    i=10
    while [ ${i} -gt 0 ];
    do
        echo "$i seconds remaining before reboot (Press control-c to abort)";
            i=$((${i} - 1))
        sleep 1;
    done
    action reboot
}
##########################################################################
# Generate VERSION file
generateVersionFile ()
{
    echo "{\"date\":\"${REMOTECOMMITDATE}\",\"branch\":\"${BRANCH}\",\"commit\":\"${REMOTECOMMITID}\"}" > $VERSION_FILE
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
            _FORCEREBOOT=1
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
        -s | --steps)
            _PROGRESS=1;
           shift
           ;;
        -r | --branch)
	    BRANCH=$2
	    shift
            shift
           ;;
        *|-h |\? | --help)
            usage $0
            exit 1
            ;;
    esac
done

log "Starting AutoUpdate on branch ${BRANCH}"

######################################################""
# Get date and last commit ID from Github
$(${CURL} -s ${GITHUBURL}/${REPO}/commits/${BRANCH} --output $COMMITS_FILE)
REMOTECOMMITDATE=$(${JQ} -r '.commit .author .date' ${COMMITS_FILE})
REMOTECOMMITID=$(${JQ} -r '.sha[0:7]' ${COMMITS_FILE} )

if [ ${_FORCE} = 1 ]; then
    log "Forcing update."
fi

if [ ${_PRINTONLY} = 1 ]; then
    log "Print actions only, do nothing."
fi

if [ ${_BACKUP} = 1 ]; then
  log "Backing up files."
fi

action "rm -rf ${DESTOVERRIDE} 2>/dev/null"

if [ -f "$VERSION_FILE" ]; then
    LOCALCOMMITID=$(${JQ} -r .commit ${VERSION_FILE})  
    if [ ${LOCALCOMMITID} = ${REMOTECOMMITID} ]; then
        logerror "You are currently on the latest version"
        echo "You are currently on the latest version"
        exit 1
    else
        echo "Need to upgrade from ${LOCALCOMMITID} to ${REMOTECOMMITID}"
        log "Getting list of remote files."
        FILES=$(${CURL} -s ${GITHUBURL}/${REPO}/compare/${LOCALCOMMITID}...${REMOTECOMMITID} | ${JQ} -r '.files[].raw_url' | grep ${REMOTEFOLDER})        
    fi
else
    echo "Version file missing. Upgrade to last commit ${REMOTECOMMITID}"
    log "Getting list of remote files."
    FIRST=$(${CURL} -s ${GITHUBURL}/${REPO}/contents/${REMOTEFOLDER}?ref=${BRANCH})
    FILES=$(getfiles "${FIRST}")
fi

if [ $_PROGRESS = 1 ]; then
   _NBTOTALFILES=$(echo $FILES | wc -w)
   log Number of file to update $_NBTOTALFILES
   echo -n 0 > /tmp/progress
fi

# For all the repository files
for i in ${FILES}
do
    progress
    # String to remove to get the local path
    LOCALFILE=$(echo ${i} | awk -F ${REMOTEFOLDER}/ '{print $2}')
    # Remove files that match the filter
    res=$(ismatch ${LOCALFILE})
    if [ "$res" == "match" ]; then
        echo "${LOCALFILE} is excluded due to filter."
        continue
    fi
    # Get the file temporally to calculate SHA
    ${CURL} -s ${i} -o ${TMPFILE} 2>/dev/null
    if [ ! -f ${TMPFILE} ]; then
        echo "Can not get remote file $i, exiting."
        exit 1
    fi
    # sometimes zero byte files are received, which overwrite the local files, we ignore those files
    # exception: files that are hidden i.e. start with dot. Ex: files like ".gitkeep"
    if [[ ! -s ${TMPFILE} ]] && [[ $(basename ${LOCALFILE} | cut -c1-1) != "." ]]; then                
        echo "Received zero byte file $i, exiting."                                                    
        exit 1                                                                                         
    fi         
    # Check the file exists in local
    if [ -f "${DESTFOLDER}/${LOCALFILE}" ]; then
        REMOTESHA=$(${SHA} ${TMPFILE} 2>/dev/null | cut -d "=" -f 2)
        # Calculate the remote and local SHA
        LOCALSHA=$(${SHA} ${DESTFOLDER}${LOCALFILE} 2>/dev/null | cut -d "=" -f 2)

        # log "SHA of $LOCALFILE is ${LOCALSHA} ** remote is ${REMOTESHA}"
        if [ "${REMOTESHA}" = "${LOCALSHA}" ] ; then
            echo "${LOCALFILE} is up to date."
        else
            if [ ${_FORCE} = 1 ]; then
                echo "${LOCALFILE} updated."
                action "mkdir -p $(dirname ${DESTOVERRIDE}/${LOCALFILE}) 2>/dev/null"
                if [ ${_BACKUP} = 1 ]; then
                    action cp ${DESTFOLDER}${LOCALFILE} ${DESTOVERRIDE}/${LOCALFILE}${BACKUPEXT}
                fi
                action mv ${TMPFILE} ${DESTOVERRIDE}/${LOCALFILE}
            else
                echo "${LOCALFILE} needs to be updated. Overwrite?"
                        echo "[Y]es or [N]o or [A]ll?"
                rep=$(ask_yes_or_no )
                if [ "${rep}" = "no" ]; then
                    echo "${LOCALFILE} not updated"
                    rm -f ${TMPFILE} 2>/dev/null
                else
                    action "mkdir -p $(dirname ${DESTOVERRIDE}/${LOCALFILE}) 2>/dev/null"
                    if [ ${_BACKUP} = 1 ]; then
                        action cp ${DESTFOLDER}${LOCALFILE} ${DESTOVERRIDE}/${LOCALFILE}${BACKUPEXT}
                    fi
                    action mv ${TMPFILE} ${DESTOVERRIDE}/${LOCALFILE}

                fi
                if [ "${rep}" = "all" ]; then
                    _FORCE=1
                fi
            fi
        fi
    else
        if [ ${_FORCE} = 1 ]; then
            echo "${LOCALFILE} created."
            action "mkdir -p $(dirname ${DESTOVERRIDE}/${LOCALFILE}) 2>/dev/null"
            action mv ${TMPFILE} ${DESTOVERRIDE}/${LOCALFILE}
        else
            echo "${LOCALFILE} doesn't exist, create it?"
            echo "[Y]es or [N]o or [A]ll ?"
            rep=$(ask_yes_or_no )
            if [ "${rep}" = "no" ]; then
                echo "${LOCALFILE} not created."
                rm -f ${TMPFILE} 2>/dev/null
            else
                action "mkdir -p $(dirname ${DESTOVERRIDE}/${LOCALFILE}) 2>/dev/null"
                action mv ${TMPFILE} ${DESTOVERRIDE}/${LOCALFILE}
            fi
            if [ "${rep}" = "all" ]; then
                _FORCE=1
            fi
        fi
    fi
done

if [ $_PROGRESS = 1 ]; then
   echo -n 100 > /tmp/progress
fi


if [ -d ${DESTOVERRIDE} ] && [ $(ls -l ${DESTOVERRIDE}/* | wc -l 2>/dev/null) > 1 ]; then
    echo "--------------- Stopping services ---------"
    for i in /system/sdcard/controlscripts/*; do
        echo stopping $i
        $i stop &> /dev/null
    done
    pkill lighttpd.bin 2> /dev/null
    pkill bftpd  2> /dev/null

    echo "--------------- Updating files ----------"
    action "cp -Rf ${DESTOVERRIDE}/* ${DESTFOLDER} 2>/dev/null"
    action "rm -Rf ${DESTOVERRIDE}/* 2>/dev/null"

    # Everythings was OK, save the date
    generateVersionFile
    echo "---------------    Reboot    ------------"
    if [ ${_FORCEREBOOT} = 1 ]; then
        countdownreboot
    else
        echo "A reboot is needed, do you want to reboot now?"
        echo "[Y]es or [N]o"
        rep=$(ask_yes_or_no )
        if [ "${rep}" = "yes" ]; then
            countdownreboot
        fi
    fi
else
    generateVersionFile
    echo "No files to update."
fi
