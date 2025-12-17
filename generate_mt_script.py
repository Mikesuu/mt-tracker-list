import requests
import re

# 你的来源 URL
urls = [
    "https://raw.githubusercontent.com/adysec/tracker/master/tracker_all.txt",
    "https://raw.githubusercontent.com/ngosang/trackerslist/master/trackers_all.txt"
]

def get_trackers():
    trackers = set()
    for url in urls:
        try:
            print(f"Fetching: {url}")
            response = requests.get(url, timeout=15)
            # 提取域名或 IP 端口前的部分
            # 支持 udp://, http://, https:// 等格式
            found = re.findall(r'(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}|(?:\d{1,3}\.){3}\d{1,3}', response.text)
            trackers.update(found)
        except Exception as e:
            print(f"Error fetching {url}: {e}")
    return sorted(list(trackers))

def save_to_rsc(tracker_list):
    with open("tracker_list.rsc", "w") as f:
        # 头部声明
        f.write("# Generated MikroTik Tracker List\n")
        f.write("/ip firewall address-list\n")
        
        # 批量删除旧条目，防止重复和冗余
        f.write("remove [find list=bt_trackers]\n")
        
        for item in tracker_list:
            # 去除 github 这种无关域名（如果正则误抓）
            if "github" in item or "google" in item:
                continue
            # MikroTik 允许直接将域名放入 address-list，它会自动解析
            f.write(f"add address={item} list=bt_trackers comment=bitcomet_tracker\n")

if __name__ == "__main__":
    trackers = get_trackers()
    save_to_rsc(trackers)
    print(f"Success! Generated {len(trackers)} trackers.")
