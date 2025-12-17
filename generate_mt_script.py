import requests
import re

# 定义来源 URL
urls = [
    "https://raw.githubusercontent.com/adysec/tracker/master/tracker_all.txt",
    "https://raw.githubusercontent.com/ngosang/trackerslist/master/trackers_all.txt"
]

def get_ips():
    ips = set()
    for url in urls:
        try:
            response = requests.get(url, timeout=10)
            # 使用正则提取域名或 IP
            # 匹配 http/https/udp 链接中的主机部分
            found = re.findall(r'(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}|(?:\d{1,3}\.){3}\d{1,3}', response.text)
            ips.update(found)
        except:
            continue
    return sorted(list(ips))

def save_rsc(ip_list):
    with open("tracker_list.rsc", "w") as f:
        f.write("/ip firewall address-list\n")
        # 清理旧列表
        f.write("remove [find list=bt_trackers]\n")
        for ip in ip_list:
            # MikroTik 会自动解析域名为 IP
            f.write(f"add address={ip} list=bt_trackers timeout=1d\n")

if __name__ == "__main__":
    ips = get_ips()
    save_rsc(ips)
    print(f"Total trackers: {len(ips)}")
