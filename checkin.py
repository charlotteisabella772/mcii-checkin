import os
import requests

def checkin():
    # 从 GitHub Secrets 中获取保存的 Cookie
    cookie = os.getenv("USER_COOKIE")
    if not cookie:
        print("❌ 未配置 USER_COOKIE 环境变量！")
        return

    url = "https://proxy.mcii.cc/api/me/checkin"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Content-Type": "application/json",
        "Cookie": cookie,
        "Referer": "https://proxy.mcii.cc/"
    }

    try:
        # 发送 POST 请求，Body 为 "{}"
        response = requests.post(url, headers=headers, json={})
        print(f"HTTP 状态码: {response.status_code}")
        print(f"接口返回内容: {response.text}")
        
        if response.status_code == 200:
            print("✅ 签到请求已成功发送！")
        else:
            print("⚠️ 响应状态异常，请检查 Cookie 是否失效或格式不正确。")
    except Exception as e:
        print(f"❌ 请求发生异常: {e}")

if __name__ == "__main__":
    checkin()
