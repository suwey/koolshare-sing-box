#!/bin/sh

alias echo_date='echo $(date "+%b %e %H:%M:%S")'
source /koolshare/scripts/base.sh

_LOG "M99sing.sh start sing-box..."
/jffs/sing-box/singbox.sh start
