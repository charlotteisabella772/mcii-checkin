import os
import requests

def checkin():
    # 从 GitHub Secrets 中获取保存的 Cookie
    cookie = os.getenv("USER_COOKIE")
    if not cookie:
        print("❌ 未配置 USER_COOKIE 环境变量！")
        return

    # 注意：新版接口去掉了 /api 前缀
    url = "https://proxy.mcii.cc/me/checkin"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Content-Type": "application/json",
        "Cookie": cookie,
        "Referer": "https://proxy.mcii.cc/"
    }

    # 新版接口要求 body 里带 confirm_partial 字段
    payload = {"confirm_partial": False}

    try:
        response = requests.post(url, headers=headers, json=payload)
        print(f"HTTP 状态码: {response.status_code}")
        print(f"接口返回内容: {response.text}")

        if response.status_code == 200:
            data = response.json()
            # 服务器可能要求二次确认
            if data.get("needs_confirmation"):
                print("⚠️ 服务器要求二次确认（needs_confirmation），签到未完成。")
                print("   需要手动到网页上确认，或改用 confirm_partial=true 重试一次。")
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
