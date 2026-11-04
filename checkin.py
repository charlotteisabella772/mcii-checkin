import os
import sys
import requests

URL = "https://proxy.mcii.cc/api/v1/me/checkin"


def fail(message):
    print(message, file=sys.stderr)
    raise SystemExit(1)


def checkin():
    cookie = os.getenv("USER_COOKIE")
    if not cookie:
        fail("❌ 未配置 USER_COOKIE 环境变量。")

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
        "Content-Type": "application/json",
        "Cookie": cookie,
        "Referer": "https://proxy.mcii.cc/",
        "Origin": "https://proxy.mcii.cc",
    }
    # Keep this false: the site must be manually confirmed before partial check-in.
    payload = {"confirm_partial": False}

    try:
        response = requests.post(URL, headers=headers, json=payload, timeout=30)
    except requests.RequestException as exc:
        fail(f"❌ 请求失败：{exc}")

    print(f"HTTP 状态码: {response.status_code}")
    if response.status_code != 200:
        fail("❌ 签到接口未成功返回（HTTP 状态码非 200）。")

    try:
        data = response.json()
    except ValueError:
        fail("❌ 接口返回的不是有效 JSON，无法确认签到结果。")

    if data.get("needs_confirmation"):
        print("⚠️ 服务器要求确认部分签到；本次签到尚未完成。")
        for item in data.get("skipped") or []:
            source_id = item.get("source_id", "未知")
            reason = item.get("reason", "原因未提供")
            print(f"   跳过来源 {source_id}: {reason}")
        fail("请先登录网站手动确认，再重新运行 GitHub Action。")

    if data.get("awarded"):
        print("✅ 签到成功！")
        print(f"   经验 +{data.get('xp_added', 0)}，积分 +{data.get('points_added', 0)}")
    else:
        print("ℹ️ 接口返回 HTTP 200，但没有报告奖励；请到网站查看签到状态。")


if __name__ == "__main__":
    checkin()
