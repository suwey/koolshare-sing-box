#!/bin/bash

CGO_ENABLED=0 GOOS=linux GOARCH=arm64 go build \
    -trimpath \
    -ldflags "-X 'github.com/sagernet/sing-box/constant.Version=1.13.11-router' -X internal/godebug.defaultGODEBUG=multipathtcp=0 -checklinkname=0 -s -w -buildid=" \
    -tags "with_gvisor,with_quic,with_dhcp,with_wireguard,with_utls,with_acme,with_clash_api,with_tailscale,with_ccm,with_ocm,badlinkname,tfogo_checklinkname0" \
    ./cmd/sing-box
