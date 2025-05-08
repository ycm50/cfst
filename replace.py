import argparse
import csv
import sys
from urllib.parse import urlparse, urlunparse

def parse_vless_link(link):
    """解析vless链接中的关键部分"""
    if not link.startswith('vless://'):
        return None
    
    # 移除协议头
    link_part = link[len('vless://'):]
    
    # 找到@的位置
    at_pos = link_part.find('@')
    if at_pos == -1:
        return None
    
    # 提取@前面的部分（UUID）
    uuid = link_part[:at_pos]
    
    # 提取@后面的部分（地址信息）
    address_part = link_part[at_pos+1:]
    
    # 解析地址部分
    try:
        parsed_url = urlparse('http://' + address_part)
        host = parsed_url.hostname
        port = parsed_url.port
        path = parsed_url.path
        query = parsed_url.query
    except:
        return None
    
    # 提取#后面的部分（备注）
    hash_pos = address_part.find('#')
    if hash_pos != -1:
        remark = address_part[hash_pos+1:]
    else:
        remark = ''
    
    return {
        'uuid': uuid,
        'host': host,
        'port': port,
        'path': path,
        'query': query,
        'remark': remark
    }

def build_vless_link(parsed_link, new_host):
    """根据解析后的信息和新主机构建vless链接"""
    if new_host.count(':') > 1:  # 判断是否为 IPv6 地址
        host_port = f"[{new_host}]:{parsed_link['port']}"
    else:
        host_port = f"{new_host}:{parsed_link['port']}"
    
    address_part = f"{host_port}{parsed_link['path']}"
    
    if parsed_link['query']:
        address_part = f"{address_part}?{parsed_link['query']}"
    
    if parsed_link['remark']:
        address_part = f"{address_part}#{parsed_link['remark']}"
    
    return f"vless://{parsed_link['uuid']}@{address_part}"

def main():
    parser = argparse.ArgumentParser(description='替换vless链接中的IP地址或域名')
    parser.add_argument('vless_link', help='要替换的vless链接')
    parser.add_argument('--csv-file', default='result.csv', help='包含替换IP的CSV文件路径，默认为当前目录下的result.csv')
    
    args = parser.parse_args()
    
    # 解析原始vless链接
    parsed_link = parse_vless_link(args.vless_link)
    if not parsed_link:
        print("无效的vless链接格式", file=sys.stderr)
        sys.exit(1)
    
    # 读取CSV文件并获取IP列表
    ip_list = []
    try:
        with open(args.csv_file, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # 尝试从不同的列中获取IP地址
                if 'IP 地址' in row and row['IP 地址']:
                    ip = row['IP 地址'].strip()
                    ip_list.append(ip)
                elif 'IP' in row and row['IP']:
                    ip = row['IP'].strip()
                    ip_list.append(ip)
    except FileNotFoundError:
        print(f"未找到CSV文件: {args.csv_file}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"读取CSV文件时出错: {e}", file=sys.stderr)
        sys.exit(1)
    
    # 生成替换后的链接
    for ip in ip_list:
        new_link = build_vless_link(parsed_link, ip)
        print(new_link)

if __name__ == '__main__':
    main()

