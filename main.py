import os
import requests, sys, time

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")  # Must be set in GitHub Secrets or OS environment
if not BOT_TOKEN:
    print("\033[31m[!] Bot token not found. Set TELEGRAM_BOT_TOKEN in environment variables.\033[0m")
    sys.exit(1)

CHANNEL_ID = "-1002162858751"
CHANNEL_USERNAME = "@unsely"
API = f"https://api.telegram.org/bot{BOT_TOKEN}"

red = "\033[31m"
green = "\033[32m"
cyan = "\033[36m"
reset = "\033[0m"

def get_user_id():
    while True:
        try:
            return int(input(f"{green}Enter your Telegram User ID:{cyan} "))
        except ValueError:
            print(f"{red}Invalid input. Please enter a numeric Telegram User ID.{reset}")

def get_chat_member(chat, user):
    try:
        r = requests.get(f"{API}/getChatMember", params={"chat_id": chat, "user_id": user}, timeout=10)
        return r.json()
    except Exception as e:
        return {"ok": False, "description": str(e)}

def check_membership(user_id):
    data = get_chat_member(CHANNEL_ID, user_id)
    if not data.get("ok") or data.get("result", {}).get("status", "") not in ("creator", "administrator", "member"):
        print(f"{red}[✖] Access Denied.{reset}")
        print(f"{cyan}Please join our official Telegram channel {CHANNEL_USERNAME} and restart the tool.{reset}")
        print(f"{cyan}Join Link: https://t.me/{CHANNEL_USERNAME.replace('@','')}{reset}")
        sys.exit(0)
    print(f"{green}[✔] Access Granted. Verified member of {CHANNEL_USERNAME}.{reset}")

print(f"{cyan}Telegram Channel Access Verification{reset}")
ID = get_user_id()
print(f"{cyan}Verifying access for User ID: {ID}...{reset}")
time.sleep(0.6)
check_membership(ID)
print(f"{green}Membership verified successfully. You may now use this tool.{reset}")
time.sleep(0.6)

print(f"{green}Starting main tool...{reset}")
