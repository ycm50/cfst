#!/bin/bash

# 下载文件并保存为 ipv6.txt
curl https://www.baipiao.eu.org/cloudflare/ips-v6 -o ipv6.txt

# 检查文件是否下载成功
if [ -f "ipv6.txt" ]; then
    # 随机选择三行写入 ip.txt
    shuf -n 3 ipv6.txt > ip.txt
    echo "已从 ipv6.txt 中随机选择三行写入 ip.txt"
else
    echo "文件下载失败"
fi

