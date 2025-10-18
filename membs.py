import requests, sys, json, os, time

BOT_TOKEN = "7391593372:AAFhLbgDhxgNmMZwlLIzB1VuxNnxykV83XQ"
CHANNEL_ID = "-1002162858751"
CHANNEL_USERNAME = "@unsely"
USER_FILE = "user_id.json"

API = f"https://api.telegram.org/bot{BOT_TOKEN}"

red = "\033[31m"
green = "\033[32m"
cyan = "\033[36m"
reset = "\033[0m"

def get_user_id():
    if os.path.exists(USER_FILE):
        try:
            with open(USER_FILE, "r") as f:
                data = json.load(f)
                if "ID" in data:
                    return int(data["ID"])
        except:
            pass
    while True:
        try:
            user_id = int(input(f"{green}Enter your Telegram User ID:{cyan} "))
            with open(USER_FILE, "w") as f:
                json.dump({"ID": user_id}, f)
            return user_id
        except ValueError:
            print(f"{red}Invalid input. Please enter numbers only.{reset}")

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
            err = data.get("description", "Unknown error")
            if "PARTICIPANT_ID_INVALID" in err or "chat not found" in err:
                continue
            return {"joined": False, "status": None, "error": err}
        result = data.get("result", {})
        status = result.get("status")
        joined = status in ("creator", "administrator", "member")
        return {"joined": joined, "status": status, "error": None}
    return {"joined": False, "status": None, "error": "User not accessible or bot not in channel."}

def main():
    print(f"{cyan}Telegram Channel Access Verification{reset}")
    uid = get_user_id()
    print(f"{cyan}Checking access for User ID: {uid}...{reset}")
    time.sleep(0.5)
    res = check_membership(uid)
    if res["error"]:
        print(f"{red}[!] Error: {res['error']}{reset}")
        return
    if res["joined"]:
        print(f"{green}[✔] Access Granted. You are a verified member of {CHANNEL_USERNAME}.{reset}")
    else:
        print(f"{red}[✖] Access Denied.{reset}")
        print(f"{cyan}Please join our official Telegram channel {CHANNEL_USERNAME} and restart this tool to continue.{reset}")

if __name__ == "__main__":
    main()
