
import requests, sys, time

BOT_TOKEN = "7391593372:AAFhLbgDhxgNmMZwlLIzB1VuxNnxykV83XQ"
CHANNEL_ID = "-1002162858751"
CHANNEL_USERNAME = "@unsely"

API = f"https://api.telegram.org/bot{BOT_TOKEN}"

red = "\033[31m"
green = "\033[32m"
cyan = "\033[36m"
reset = "\033[0m"

def get_chat_member(chat, user):
    try:
        r = requests.get(f"{API}/getChatMember", params={"chat_id": chat, "user_id": user}, timeout=10)
        return r.json()
    except Exception as e:
        return {"ok": False, "description": str(e)}

def check_membership(user_id):
    chats = [CHANNEL_ID, CHANNEL_USERNAME]
    for chat in chats:
        data = get_chat_member(chat, user_id)
        if not data.get("ok"):
            err = data.get("description", "")
            if "PARTICIPANT_ID_INVALID" in err or "chat not found" in err:
                continue
            return {"joined": False, "error": err}
        status = data.get("result", {}).get("status")
        return {"joined": status in ("creator", "administrator", "member"), "error": None}
    return {"joined": False, "error": "Bot not in channel or user not accessible."}

def main():
    print(f"{cyan}Telegram Channel Access Verification{reset}")
    try:
        user_id = int(input(f"{green}Enter your Telegram User ID:{cyan} ").strip())
    except ValueError:
        print(f"{red}Invalid input. Please enter a numeric Telegram User ID.{reset}")
        sys.exit()
    print(f"{cyan}Verifying access for User ID: {user_id}...{reset}")
    time.sleep(0.6)
    res = check_membership(user_id)
    if res["error"]:
        print(f"{red}[!] Error: {res['error']}{reset}")
        sys.exit()
    if res["joined"]:
        print(f"{green}[✔] Access Granted. You are a verified member of {CHANNEL_USERNAME}.{reset}")
    else:
        print(f"{red}[✖] Access Denied.{reset}")
        print(f"{cyan}Please join our official Telegram channel {CHANNEL_USERNAME} to continue using this tool.{reset}")
        print(f"{cyan}Join Link: https://t.me/{CHANNEL_USERNAME.replace('@','')}{reset}")
        sys.exit()

if __name__ == "__main__":
    main()
