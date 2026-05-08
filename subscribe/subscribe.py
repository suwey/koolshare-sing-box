#!/usr/bin/env python3

import argparse
import requests
import base64
import json
import os
from urllib.parse import unquote, urlparse, parse_qs

def down_source(url, source_down):
    try:
        text = requests.get(url).text
    except Exception as e:
        print(f"获取订阅失败: {e}")
        exit(1)

    # 用网页内容生成节点
    with open(source_down, "w") as f:
        f.write(text)


def decode_source(source_down, source_decode):
    # 读取输入文件
    with open(source_down, 'r', encoding='utf-8') as f:
        content = f.read().strip()

    # 第一步: Base64解码
    try:
        decoded_bytes = base64.b64decode(content)
    except Exception as e:
        print(f"Base64解码失败: {e}")
        exit(1)

    # 第二步: URL解码
    try:
        # 先尝试用UTF-8解码字节，再进行URL解码
        intermediate = decoded_bytes.decode('utf-8')
        final_result = unquote(intermediate)
    except UnicodeDecodeError:
        # 如果UTF-8失败，尝试直接用URL解码（某些情况可能是原始字节）
        try:
            final_result = unquote(decoded_bytes.decode('latin-1'))
        except Exception as e:
            print(f"URL解码失败: {e}")
            exit(1)
    except Exception as e:
        print(f"解码失败: {e}")
        exit(1)

    # 写入输出文件
    with open(source_decode, 'w', encoding='utf-8') as f:
        f.write(final_result)


def parse_anytls_url(line):
    """解析 anytls:// URL，返回 node 字典"""
    line = line.strip()
    if not line:
        return None

    node = {
        "tag": "",
        "type": "anytls",
        "server": "",
        "server_port": 0,
        "password": "",
        "tls": {
            "enabled": True,
            "server_name": "",
            "insecure": False,
            "utls": {
                "enabled": True,
                "fingerprint": "chrome"
            },
            "alpn": [
                "h2",
                "http/1.1"
            ]
        },
        "idle_session_check_interval": "60s",
        "idle_session_timeout": "300s",
        "min_idle_session": 1
    }

    try:
        parsed = urlparse(line)

        if parsed.scheme != "anytls":
            print(f"  跳过非 anytls 链接: {line[:50]}...")
            return None

        # password
        node["password"] = parsed.path.lstrip("/")

        # server 和 port
        netloc = parsed.netloc
        if "@" in netloc:
            node["password"] = netloc.split("@", 1)[0]
            netloc = netloc.split("@", 1)[1]

        if ":" in netloc:
            host_port = netloc.rsplit(":", 1)
            node["server"] = host_port[0]
            node["server_port"] = int(host_port[1])
        else:
            node["server"] = netloc

        # 查询参数
        query_params = parse_qs(parsed.query)

        # sni
        if "sni" in query_params:
            node["tls"]["server_name"] = query_params["sni"][0]

        # insecure: 0=false, 1=true
        if "insecure" in query_params:
            node["tls"]["insecure"] = (query_params["insecure"][0] == "1")

        # tag
        if parsed.fragment:
            node["tag"] = parsed.fragment

    except Exception as e:
        print(f"  解析失败: {line[:50]}... 错误: {e}")
        return None

    return node


def parse_nodes(source_decode, nodes_json, filters):
    selector = {
        "tag": "🚀FinalOut",
        "type": "urltest",
        "interrupt_exist_connections": False,
        "interval": "30s",
        "idle_timeout": "1440m"
    }
    selector['outbounds'] = []
    o = []

    with open(source_decode, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    print(f"共 {len(lines)} 行，开始解析...")

    o.append(selector)
    for i, line in enumerate(lines, 1):
        node = parse_anytls_url(line)
        if node:
            if len(filters) > 0:
                for filter in filters:
                    if filter in node['tag']:
                        o.append(node)
                        selector['outbounds'].append(node['tag'])
                        print(f"  [{i}] ✓ {node['tag']}")
                        break
            else:
                o.append(node)
                selector['outbounds'].append(node['tag'])
                print(f"  [{i}] ✓ {node['tag']}")


    with open(nodes_json, 'w', encoding='utf-8') as f:
        json.dump(o, f, ensure_ascii=False, indent=2)

    print(f"\n完成！共解析 {len(selector['outbounds'])} 个节点")
    print(f"输出文件: {nodes_json}")


def read_lines(path):
    """读取文件，返回非空行列表（整行为空才算空行，保留原样）"""
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    return [line for line in lines if line.strip()]

def read_nodes(path):
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    if len(lines) > 2:
        lines = lines[1:-1]

    result = [line for line in lines if line.strip()]

    if len(result) < 2:
        print(f"错误: 没有获取到有效节点！")
        exit(1)

    result = [f"  {r}" for r in result]
    result[0] = "\n" + result[0]
    result[-1] = result[-1] + ","

    return result


def main():
    parser = argparse.ArgumentParser(description='从订阅链接生成config.json')
    parser.add_argument('-u', '--url', required=True, help='输入订阅链接')
    parser.add_argument('-o', '--output', required=False, help='输入生成的配置文件名，默认为"config.json"')
    parser.add_argument('-f', '--filter', action='append', dest='filters', default=[], required=False, help='按指定值过滤节点，可重复输入如"-f 高速隧道1x-香港 -f 专线2.5"')

    args = parser.parse_args()
    output = args.output if args.output else "config.json"
    files = ["soource_down", "source_decode", "nodes.json"]
    down_source(args.url, files[0])
    decode_source(files[0], files[1])
    parse_nodes(files[1], files[2], args.filters)

    for f in files:
        if not os.path.exists(f):
            print(f"错误: 中间步骤文件不存在 - {f}")
            exit(1)

    out_lines = []

    # 1. 读 config-head.json
    head_lines = read_lines("config-head.json")
    out_lines.extend(head_lines[:-1])
    out_lines.extend('  "outbounds": [')

    # 2. 读 nodes.json（跳过首尾行）
    node_lines = read_nodes(files[2])
    out_lines.extend(node_lines[:-1])
    out_lines.extend("    },\n")

    # 3. 读 config-end.json
    end_lines = read_lines("config-end.json")
    out_lines.extend(end_lines)

    # 4. 写入 config.json
    with open(output, "w", encoding="utf-8") as f:
        f.writelines(out_lines)

    print(f"\n✓ 合成完成: {output} ({len(out_lines)} 行)")

    for f in files:
        if os.path.exists(f):
            os.remove(f)


if __name__ == '__main__':
    main()
