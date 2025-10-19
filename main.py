import requests
import sys
import time

# Updated API endpoint
API_URL = "https://dumb-members-checker-api.vercel.app/api/"

# Channel name for message
CHANNEL_NAME = "@unsely"

# Color codes
RED = "\033[31m"
GREEN = "\033[32m"
CYAN = "\033[36m"
RESET = "\033[0m"

def get_user_id():
    while True:
        try:
            return int(input(f"{GREEN}Enter your Telegram User ID: {CYAN}"))
        except ValueError:
            print(f"{RED}Invalid input. Please enter a numeric Telegram User ID.{RESET}")

def check_membership(user_id):
    try:
        response = requests.get(API_URL, params={"user_id": user_id}, timeout=10)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as e:
        print(f"{RED}[✖] Failed to reach API: {e}{RESET}")
        sys.exit(1)
    except ValueError:
        print(f"{RED}[✖] Invalid JSON response from API.{RESET}")
        sys.exit(1)

    # Check membership
    if data.get("ok") and data.get("member"):
        print(f"{GREEN}[✔] Access Granted: User is a member ({data.get('status')}){RESET}")
    else:
        # Custom friendly message for all denial reasons
        print(f"{RED}[✖] Access Denied: Please join required channel {CHANNEL_NAME} so you can use this tool.{RESET}")
        sys.exit(0)

print(f"{CYAN}Telegram Channel Access Verification via Vercel API{RESET}")
user_id = get_user_id()
print(f"{CYAN}Verifying access for User ID: {user_id}...{RESET}")
time.sleep(0.5)
check_membership(user_id)
print(f"{GREEN}Membership verified successfully. You may now use this tool.{RESET}")
time.sleep(0.5)
print(f"{GREEN}Starting main tool...{RESET}")
