# koolshare-sing-box

---

Run sing-box in a koolshare router like ac86u


1. On router:
```
mkdir -p /jffs/sing-box/ui
```
Prepare [metacubexd](https://github.com/MetaCubeX/metacubexd/releases/download/v1.246.3/compressed-dist.tgz) for ui, extract and copy all contents to /jffs/sing-box/ui/

Prepare [sing-box](https://github.com/SagerNet/sing-box/releases/download/v1.13.11/sing-box-1.13.11-linux-arm64-musl.tar.gz), extract and copy sing-box to /jffs/sing-box/

2. On computer, fill your own nodes in config.json then:
```
scp -O singbox.sh 192.168.1.1:/jffs/sing-box/
scp -O config.json 192.168.1.1:/jffs/sing-box/
scp -O M99sing.sh 192.168.1.1:/koolshare/init.d/
```
3. On router:
```
chmod +x /jffs/sing-box/singbox.sh /koolshare/init.d/M99sing.sh
```
4. Reboot router and see http://192.168.1.1:9090/ui/#/overview.

---

The subscribe.py only parse anytls node.
