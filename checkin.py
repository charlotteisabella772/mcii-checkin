import os
import requests

def checkin():
    # 从 GitHub Secrets 中获取保存的 Cookie
    cookie = os.getenv("USER_COOKIE")
    if not cookie:
        print("❌ 未配置 USER_COOKIE 环境变量！")
        return

    # 新版接口前缀是 /api/v1
    url = "https://proxy.mcii.cc/api/v1/me/checkin"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Content-Type": "application/json",
        "Cookie": cookie,
        "Referer": "https://proxy.mcii.cc/",
        "Origin": "https://proxy.mcii.cc",
    }

    # 新版接口要求 body 里带 confirm_partial 字段
    payload = {"confirm_partial": False}

    try:
        response = requests.post(url, headers=headers, json=payload)
        print(f"HTTP 状态码: {response.status_code}")
        print(f"接口返回内容: {response.text}")

        if response.status_code == 200:
            try:
                data = response.json()
            except Exception:
                print("✅ 请求成功（响应不是 JSON）")
                return

            if data.get("needs_confirmation"):
                print("⚠️ 服务器要求二次确认（needs_confirmation），签到未完成。")
                print("   需要先到网页上手动确认一次。")
            else:
                print("✅ 签到成功！")
                if data.get("awarded"):
                    print(f"   经验 +{data.get('xp_added')}，积分 +{data.get('points_added')}")
        else:
            print(f"⚠️ 状态码 {response.status_code}，响应：{response.text}")
    except Exception as e:
        print(f"❌ 请求发生异常: {e}")

if __name__ == "__main__":
    checkin()
