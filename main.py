import requests
import sys
import time

# -------------------------------
# Vercel API URL
# -------------------------------
API_URL = "https://your-vercel-project.vercel.app/api"

# -------------------------------
# Console colors
# -------------------------------
RED = "\033[31m"
GREEN = "\033[32m"
CYAN = "\033[36m"
RESET = "\033[0m"

# -------------------------------
# Get User ID
# -------------------------------
def get_user_id():
    while True:
        try:
            return int(input(f"{GREEN}Enter your Telegram User ID: {CYAN}"))
        except ValueError:
            print(f"{RED}Invalid input. Please enter a numeric Telegram User ID.{RESET}")

# -------------------------------
# Check membership via PHP API
# -------------------------------
def check_membership(user_id):
    try:
        # GET request to API
        response = requests.get(API_URL, params={"userid": user_id}, timeout=10)
        text = response.text.strip()
    except requests.RequestException as e:
        print(f"{RED}[✖] Failed to reach API: {e}{RESET}")
        sys.exit(1)

    if "✅" in text:
        print(f"{GREEN}[✔] Access Granted: {text}{RESET}")
    else:
        print(f"{RED}[✖] Access Denied: {text}{RESET}")
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
