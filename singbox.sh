#!/bin/bash
# =============================================
# singbox.sh {start|stop|restart|status}
# UI: https://github.com/MetaCubeX/metacubexd/releases/download/v1.246.3/compressed-dist.tgz
# sing-box: https://github.com/SagerNet/sing-box/releases/download/v1.13.11/sing-box-1.13.11-linux-arm64-musl.tar.gz
# =============================================

SINGBOX_DIR=$(cd $(dirname $0) && pwd)
cd $SINGBOX_DIR
SINGBOX_BIN="$SINGBOX_DIR/sing-box"
CONFIG="$SINGBOX_DIR/config.json"
LOG="$SINGBOX_DIR/sing-box.log"
MEM_LIMIT="100MiB"

do_stop() {
    killall sing-box 2>/dev/null
    echo "[sing-box] stopped at $(date "+%Y-%m-%d %H:%M:%S")."
}

do_start() {
    rm -rf /dev/net
    mkdir -p /dev/net
    modprobe tun
    mknod /dev/net/tun c 10 200
    chmod 666 /dev/net/tun

    $SINGBOX_BIN check -c $CONFIG
    if [ $? -gt 0 ];then
        echo "[singbox] config invalid!"
        exit 1
    fi

    GOMEMLIMIT=$MEM_LIMIT $SINGBOX_BIN run -c $CONFIG -D $SINGBOX_DIR > $LOG 2>&1
}

case "$1" in
    start)
        do_start
        ;;
    stop)
        do_stop
        ;;
    restart)
        do_stop
        sleep 8
        do_start
        ;;
    status)
        ps | grep "sing-box" | grep -v grep
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|status}"
        exit 1
        ;;
esac
