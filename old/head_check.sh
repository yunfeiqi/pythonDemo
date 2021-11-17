
# work pach
WORK_DIR=`dirname $0`
work_path=`dirname ${WORK_DIR}`
cd $work_path

# defination
RED="\033[0;32;31m"
GREEN="\033[0;32;32m"
YELLOW="\033[1;33m"
NONE="\033[m"


ARGS_NUM=$#

COMMAND=$1

function request(){
    service=$1
    echo -e "$GREEN*************************** $service ***************************"
    echo 
    curl -i -X POST http://10.10.100.228:8044/$service \
    -H 'Content-Type: application/json'  \
    --data-binary "@service/$service.json"
    echo
    echo -e "***************************************************************$NONE"
}

function process() {
    service=$1
    if [[ x$service == 'xall' ]]; then
        for s in `ls service`;
        do
            s=`echo $s | awk '{sub(/.json/,""); print $0}'`
            request $s
            echo -e "$RED--------------------$NONE"
        done

    else
        request $service
    fi

}

function check_service() {
    service=$1
    process $service
}

if [[ x$ARGS_NUM == x"0" ]];then
    check_service all
else
    check_service $COMMAND
fi
