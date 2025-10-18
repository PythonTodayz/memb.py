import requests
import sys
import time

# -------------------------------
# Vercel API URL
# -------------------------------
API_URL = "https://bkl-gend-faad-dnga.vercel.app/api/check_membership"

# -------------------------------
# Console colors
# -------------------------------
RED = "\033[31m"
GREEN = "\033[32m"
CYAN = "\033[36m"
RESET = "\033[0m"

# -------------------------------
# Get User ID from input
# -------------------------------
def get_user_id():
    while True:
        try:
            return int(input(f"{GREEN}Enter your Telegram User ID: {CYAN}"))
        except ValueError:
            print(f"{RED}Invalid input. Please enter a numeric Telegram User ID.{RESET}")

# -------------------------------
# Check membership via Vercel API
# -------------------------------
def check_membership(user_id):
    try:
        # Send GET request to Vercel API
        response = requests.get(f"{API_URL}?userid={user_id}", timeout=10)
        data = response.json()
    except requests.RequestException as e:
        print(f"{RED}[✖] Failed to reach API: {e}{RESET}")
        sys.exit(1)
    except ValueError:
        print(f"{RED}[✖] Invalid response from API{RESET}")
        sys.exit(1)

    if data.get("ok"):
        print(f"{GREEN}[✔] Access Granted: {data.get('message', 'Joined')} for channel {data.get('channel')}{RESET}")
    else:
        print(f"{RED}[✖] Access Denied: {data.get('message', data.get('description', 'Not joined'))}{RESET}")
        print(f"{CYAN}Please join the official Telegram channel {data.get('channel', '')}{RESET}")
        print(f"{CYAN}Join Link: https://t.me/{data.get('channel','').replace('@','')}{RESET}")
        sys.exit(0)

# -------------------------------
# Main
# -------------------------------
print(f"{CYAN}Telegram Channel Access Verification via Vercel API{RESET}")
user_id = get_user_id()
print(f"{CYAN}Verifying access for User ID: {user_id}...{RESET}")
time.sleep(0.5)
check_membership(user_id)
print(f"{GREEN}Membership verified successfully. You may now use this tool.{RESET}")
time.sleep(0.5)

print(f"{GREEN}Starting main tool...{RESET}")
