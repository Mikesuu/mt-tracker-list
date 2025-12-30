import requests
import re

urls = [
    "https://raw.githubusercontent.com/ngosang/trackerslist/master/trackers_best.txt",
    "https://raw.githubusercontent.com/ngosang/trackerslist/master/trackers_all.txt",
    "https://raw.githubusercontent.com/ngosang/trackerslist/master/trackers_all_udp.txt",
    "https://raw.githubusercontent.com/ngosang/trackerslist/master/trackers_all_http.txt",
    "https://raw.githubusercontent.com/ngosang/trackerslist/master/trackers_all_https.txt",
    "https://raw.githubusercontent.com/ngosang/trackerslist/master/trackers_all_ws.txt",
    "https://raw.githubusercontent.com/ngosang/trackerslist/master/trackers_all_i2p.txt",
    "https://raw.githubusercontent.com/ngosang/trackerslist/master/trackers_all_yggdrasil.txt",
    "https://raw.githubusercontent.com/ngosang/trackerslist/master/trackers_best_ip.txt",
    "https://raw.githubusercontent.com/ngosang/trackerslist/master/trackers_all_ip.txt",
    "https://raw.githubusercontent.com/ngosang/trackerslist/master/trackers_all_yggdrasil_ip.txt",
    "https://cf.trackerslist.com/best.txt",
    "https://cf.trackerslist.com/all.txt",
    "https://cf.trackerslist.com/http.txt",
    "https://cf.trackerslist.com/nohttp.txt",
    "https://down.adysec.com/trackers_all.txt",
    "https://down.adysec.com/trackers_best.txt",
    "https://down.adysec.com/trackers_best_http.txt",
    "https://down.adysec.com/trackers_best_https.txt",
    "https://down.adysec.com/trackers_best_udp.txt",
    "https://down.adysec.com/trackers_best_wss.txt"
]

def get_trackers():
    trackers = set()
    for url in urls:
        try:
            print(f"Fetching: {url}")
            response = requests.get(url, timeout=15)
            found = re.findall(r'(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}|(?:\d{1,3}\.){3}\d{1,3}', response.text)
            trackers.update(found)
        except Exception as e:
            print(f"Error: {e}")
    return sorted(list(trackers))

def save_to_rsc(tracker_list):
    with open("tracker_list.rsc", "w") as f:
        f.write("# Generated MikroTik Tracker List\n")
        f.write("/ip firewall address-list\n")
        f.write("remove [find list=bt_trackers]\n")
        for item in tracker_list:
            if "github" in item or "google" in item:
                continue
            f.write(f"add address={item} list=bt_trackers comment=bitcomet_tracker\n")

if __name__ == "__main__":
    trackers = get_trackers()
    save_to_rsc(trackers)
    print(f"Success! Generated {len(trackers)} trackers.")
