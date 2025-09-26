import requests
import tkinter as tk
from tkinter import filedialog

# Hide the root Tkinter window
root = tk.Tk()
root.withdraw()

# ---- Translations ----
LANG = {
    "en": {
        "welcome": "Universal Webhook Sender 🚀",
        "lang_select": "Select language / เลือกภาษา (en/th): ",
        "enter_webhook": "Enter webhook URL (or leave blank for Slack API). Type 'done' when finished:",
        "slack_token": "  Enter your Slack Bot Token (xoxb-...): ",
        "slack_channel": "  Enter target Slack channel ID or name: ",
        "configured": "Configured targets:",
        "send_type": "Select send type (1: Message, 2: File): ",
        "msg_prompt": "Enter message (or 'exit' to quit): ",
        "file_prompt": "Select a file (Cancel to exit)...",
        "goodbye": "Goodbye!",
        "success_msg": "✅ {t} message sent successfully!",
        "success_file": "✅ {t} file sent successfully!",
        "fail": "❌ {t} failed: {err}",
        "slack_file_warn": "⚠️ Slack webhooks cannot upload files. Use Slack API instead.",
        "unsupported_file": "❌ {t} does not support file uploads.",
        "invalid": "Invalid selection."
    },
    "th": {
        "welcome": "โปรแกรมส่ง Webhook 🚀",
        "lang_select": "เลือกภาษา / Select language (en/th): ",
        "enter_webhook": "ใส่ลิงก์ Webhook (หรือเว้นว่างเพื่อใช้ Slack API) พิมพ์ 'done' เมื่อเสร็จ:",
        "slack_token": "  ใส่ Slack Bot Token (xoxb-...): ",
        "slack_channel": "  ใส่ Slack Channel ID หรือชื่อช่อง: ",
        "configured": "Webhook ที่ตั้งค่าแล้ว:",
        "send_type": "เลือกประเภทการส่ง (1: ข้อความ, 2: ไฟล์): ",
        "msg_prompt": "พิมพ์ข้อความ (หรือ 'exit' เพื่อออก): ",
        "file_prompt": "เลือกไฟล์ (กด Cancel เพื่อออก)...",
        "goodbye": "ลาก่อน!",
        "success_msg": "✅ ส่งข้อความไปยัง {t} สำเร็จ!",
        "success_file": "✅ ส่งไฟล์ไปยัง {t} สำเร็จ!",
        "fail": "❌ {t} ล้มเหลว: {err}",
        "slack_file_warn": "⚠️ Slack webhook ไม่รองรับการอัปโหลดไฟล์ ใช้ Slack API แทน",
        "unsupported_file": "❌ {t} ไม่รองรับการอัปโหลดไฟล์",
        "invalid": "ตัวเลือกไม่ถูกต้อง"
    }
}

# ---- Detection ----
def detect_webhook_type(url: str) -> str:
    if "discord.com/api/webhooks" in url:
        return "discord"
    elif "hooks.slack.com" in url:
        return "slack"
    elif "office.com/webhook" in url or "outlook.office.com/webhook" in url:
        return "teams"
    elif "chat.googleapis.com/v1/spaces/" in url:
        return "googlechat"
    else:
        return "generic"

# ---- Sending Handlers ----
def send_discord_message(url, message):
    return requests.post(url, json={"content": message})

def send_discord_file(url, file_path):
    with open(file_path, "rb") as f:
        return requests.post(url, files={"file": f})

def send_slack_message(url, message):
    return requests.post(url, json={"text": message})

def send_slack_file(bot_token, channels, file_path, message=None):
    headers = {"Authorization": f"Bearer {bot_token}"}
    with open(file_path, "rb") as f:
        data = {"channels": channels}
        if message:
            data["initial_comment"] = message
        files = {"file": f}
        return requests.post("https://slack.com/api/files.upload", headers=headers, data=data, files=files)

def send_slack_api_message(token, channel, message):
    return requests.post("https://slack.com/api/chat.postMessage",
                         headers={"Authorization": f"Bearer {token}"},
                         json={"channel": channel, "text": message})

def send_teams_message(url, message):
    return requests.post(url, json={"text": message})

def send_googlechat_message(url, message):
    return requests.post(url, json={"text": message})

def send_generic_message(url, message):
    return requests.post(url, json={"message": message})

# ---- Main Program ----
lang_choice = input(LANG["en"]["lang_select"]).strip().lower()
if lang_choice not in ["en", "th"]:
    lang_choice = "en"
L = LANG[lang_choice]

print("\n" + L["welcome"])
targets = []

while True:
    url = input("\n" + L["enter_webhook"] + " ").strip()
    if url.lower() == "done":
        break
    if url == "":
        slack_token = input(L["slack_token"]).strip()
        slack_channel = input(L["slack_channel"]).strip()
        targets.append({"type": "slack_api", "token": slack_token, "channel": slack_channel})
    else:
        wtype = detect_webhook_type(url)
        targets.append({"type": wtype, "url": url})

print(f"\n{L['configured']} {[t['type'] for t in targets]}")

input_type = input(L["send_type"])

# ---- Message Mode ----
if input_type == "1":
    while True:
        message = input(L["msg_prompt"])
        if message.lower() == "exit":
            break

        for t in targets:
            if t["type"] == "discord":
                response = send_discord_message(t["url"], message)
            elif t["type"] == "slack":
                response = send_slack_message(t["url"], message)
            elif t["type"] == "slack_api":
                response = send_slack_api_message(t["token"], t["channel"], message)
            elif t["type"] == "teams":
                response = send_teams_message(t["url"], message)
            elif t["type"] == "googlechat":
                response = send_googlechat_message(t["url"], message)
            else:
                response = send_generic_message(t["url"], message)

            if response is not None and response.status_code in [200, 204]:
                print(L["success_msg"].format(t=t["type"]))
            elif response is not None and "ok" in response.json() and response.json()["ok"]:
                print(L["success_msg"].format(t=t["type"]))
            else:
                print(L["fail"].format(t=t["type"], err=response.status_code if response else "Unsupported"))

# ---- File Mode ----
elif input_type == "2":
    while True:
        print(L["file_prompt"])
        file_path = filedialog.askopenfilename()
        if not file_path:
            print(L["goodbye"])
            break

        for t in targets:
            if t["type"] == "discord":
                response = send_discord_file(t["url"], file_path)
                if response.status_code in [200, 204]:
                    print(L["success_file"].format(t="Discord"))
                else:
                    print(L["fail"].format(t="Discord", err=response.status_code))
            elif t["type"] == "slack_api":
                response = send_slack_file(t["token"], t["channel"], file_path)
                if response.json().get("ok"):
                    print(L["success_file"].format(t="Slack"))
                else:
                    print(L["fail"].format(t="Slack", err=response.json()))
            elif t["type"] == "slack":
                print(L["slack_file_warn"])
            else:
                print(L["unsupported_file"].format(t=t["type"]))
else:
    print(L["invalid"])