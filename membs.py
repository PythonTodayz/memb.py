# memb.py
# Telegram channel membership checker (standalone + callable)
# Hardcoded bot token, channel id and channel username as requested (no env)
# Usage (standalone): python memb.py
# Usage (import): from memb import check_membership; result = check_membership(123456789)

import requests
import sys
import time

# ---------- CONFIG (change if you want) ----------
BOT_TOKEN = "7391593372:AAFhLbgDhxgNmMZwlLIzB1VuxNnxykV83XQ"
# You provided both a numeric chat id and a username; this script will try chat_id first then username
CHANNEL_ID = "-1002162858751"   # numeric chat id (string)
CHANNEL_USERNAME = "@unsely"    # channel username (string)
# -------------------------------------------------

API_BASE = f"https://api.telegram.org/bot{BOT_TOKEN}"

def _api_get(method, params=None, timeout=10):
    url = f"{API_BASE}/{method}"
    try:
        r = requests.get(url, params=params or {}, timeout=timeout)
        return r.json(), r.status_code
    except Exception as e:
        return {"ok": False, "error": str(e)}, 599

def is_status_member(status_str):
    # statuses considered as "joined"
    return status_str in ("creator", "administrator", "member")

def check_membership(user_id, chat_identifier=None, verbose=True):
    """
    Check Telegram membership for user_id in chat_identifier.
    - user_id: int or numeric-string (Telegram user id)
    - chat_identifier: if None, function will try CHANNEL_ID then CHANNEL_USERNAME
    Returns: dict { 'ok': bool, 'joined': bool, 'status': str or None, 'error': str or None }
    """
    if chat_identifier is None:
        try_order = [CHANNEL_ID, CHANNEL_USERNAME]
    else:
        try_order = [chat_identifier]

    # Normalize user_id
    try:
        uid = int(user_id)
    except Exception:
        return {"ok": False, "joined": False, "status": None, "error": "user_id must be numeric"}

    last_error = None
    for chat in try_order:
        params = {"chat_id": chat, "user_id": uid}
        data, code = _api_get("getChatMember", params=params)
        if not isinstance(data, dict):
            last_error = f"Bad response ({code})"
            continue

        if data.get("ok"):
            result = data.get("result", {})
            status = result.get("status")
            joined = is_status_member(status)
            if verbose:
                if joined:
                    print(f"[+] User {uid} IS a member of {chat} (status: {status}).")
                else:
                    print(f"[-] User {uid} is NOT a member of {chat} (status: {status}).")
            return {"ok": True, "joined": joined, "status": status, "error": None}
        else:
            # Telegram returned error — capture it and try next identifier if available
            err = data.get("description", data.get("error", "unknown error"))
            last_error = f"chat={chat} -> {err}"
            # If it's "chat not found" or "bot was kicked", try next; if it's rate limit, abort
            code_name = data.get("error_code")
            # if bot is not allowed, return immediate error
            if "chat not found" in str(err).lower() or "bot was kicked" in str(err).lower():
                # Try next identifier if any
                if len(try_order) > 1:
                    continue
                else:
                    return {"ok": False, "joined": False, "status": None, "error": err}
            if "too many requests" in str(err).lower() or "retry after" in str(err).lower():
                return {"ok": False, "joined": False, "status": None, "error": err}
            # otherwise continue trying next chat identifier

    # if we reached here, all tries failed
    return {"ok": False, "joined": False, "status": None, "error": last_error or "unknown error"}

def cli_prompt_and_check():
    print("Telegram Channel Membership Checker")
    print("Enter a Telegram user id to check membership (numeric).")
    try:
        user = input("User ID: ").strip()
        if not user:
            print("No user id provided. Exiting.")
            sys.exit(1)
        print("Checking membership... (this requires the bot to be admin or a member of the channel)")
        res = check_membership(user)
        if not res.get("ok"):
            print(f"[!] Error checking membership: {res.get('error')}")
            sys.exit(2)
        if res.get("joined"):
            print("[✔] User is a member — allow tool to continue.")
            # The script continues — return success code 0
            return True
        else:
            print("[✖] User is not a member — stopping the tool.")
            sys.exit(3)
    except KeyboardInterrupt:
        print("\nInterrupted.")
        sys.exit(1)

if __name__ == "__main__":
    cli_prompt_and_check()
