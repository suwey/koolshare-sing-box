# koolshare-sing-box

---

Run sing-box in a koolshare router like ac86u, enabled jffs swap. If not, may have no enough memory even when MEMLIMIT=100MiB setted in singbox.sh.


1. On router:
```
mkdir -p /jffs/sing-box/ui
```
Prepare [metacubexd](https://github.com/MetaCubeX/metacubexd/releases/download/v1.246.3/compressed-dist.tgz) for ui, extract and copy all contents to /jffs/sing-box/ui/

Prepare [sing-box](https://github.com/SagerNet/sing-box/releases/download/v1.13.11/sing-box-1.13.11-linux-arm64-musl.tar.gz) or [patch for clash api version](./changes/v1.13.11-ddb757a2/bin/sing-box.tgz), extract and copy sing-box to /jffs/sing-box/

2. On computer, change your own settings in config.json then:
```
scp -O singbox.sh 192.168.1.1:/jffs/sing-box/
scp -O config.json 192.168.1.1:/jffs/sing-box/
scp -O M99sing.sh 192.168.1.1:/koolshare/init.d/
```
Notice: support only one config file.

3. On router:
```
chmod +x /jffs/sing-box/singbox.sh /koolshare/init.d/M99sing.sh
cd /jffs/sing-box/
./singbox.sh start
```
Confirm works fine before next step, If not, just press ctrl+c and edit your config.json then start and check again.

4. Reboot router and see http://192.168.1.1:9090/ui/#/overview. If something wrong:
```
./singbox.sh stop.
```

Notice: Power cycling may cause issue!

---

## Patch for clash api
No need to reboot router for config changes, edit or scp new config to /jffs/sing-box/config.json then click "Restart Core" in UI.
