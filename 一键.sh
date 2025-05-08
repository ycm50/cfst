#!/bin/bash

chmod +x dl.sh

chmod +x cfst
# 运行dl.sh脚本
./dl.sh

# 临时禁用代理并运行cfst脚本
HTTP_PROXY= HTTPS_PROXY= ./cfst

