import os
import requests

def probe():
    cookie = os.getenv("USER_COOKIE")
    if not cookie:
        print("❌ 未配置 USER_COOKIE 环境变量！")
        return

    url = "https://proxy.mcii.cc/me/checkin"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Content-Type": "application/json",
        "Cookie": cookie,
        "Referer": "https://proxy.mcii.cc/",
        "Origin": "https://proxy.mcii.cc",
    }

    payload = {"confirm_partial": False}

    for method in ["POST", "PUT", "PATCH", "GET"]:
        try:
            if method == "GET":
                r = requests.request(method, url, headers=headers, timeout=20)
            else:
                r = requests.request(method, url, headers=headers,
                                     json=payload, timeout=20)
            print(f"--- {method} → {r.status_code}")
            print(f"    {r.text[:300]}")
        except Exception as e:
            print(f"--- {method} → 异常: {e}")

if __name__ == "__main__":
    probe()
