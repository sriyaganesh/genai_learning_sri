import pyautogui
import pyperclip
import pandas as pd
import time
from urllib.parse import quote

pyautogui.FAILSAFE = True

# Images
NEW_CHAT_IMG = "new_chat.png"
# SEARCH_BAR_IMG = "search_bar.png"

# Excel file
EXCEL_FILE = "excel_contacts.xlsx"

# Retry settings
MAX_RETRIES = 10
CONFIDENCE = 0.7
WAIT_BETWEEN_RETRIES = 2

# Function to locate and click an image with retries
def locate_and_click(image, description):
    for i in range(MAX_RETRIES):
        location = pyautogui.locateCenterOnScreen(image, confidence=CONFIDENCE)
        if location:
            pyautogui.click(location)
            time.sleep(1)
            return True
        print(f"{description} not found, retry {i+1}/{MAX_RETRIES}")
        time.sleep(WAIT_BETWEEN_RETRIES)
    print(f"Error: {description} not found after {MAX_RETRIES} retries")
    return False

def open_new_chat(phone):
    if not locate_and_click(NEW_CHAT_IMG, "New Chat button"):
        return False

    # if not locate_and_click(SEARCH_BAR_IMG, "Search bar"):
    #     return False

    pyperclip.copy(phone)
    pyautogui.hotkey("ctrl", "v")
    time.sleep(2)
    pyautogui.press("enter")
    time.sleep(2)
    print(f"Opened chat with {phone}")
    return True



def open_whatsapp():
    """Open WhatsApp Web in Edge"""
    pyautogui.hotkey("win", "r")
    time.sleep(1)
    pyautogui.write("msedge")
    pyautogui.press("enter")
    time.sleep(5)
    pyautogui.hotkey("ctrl", "l")
    pyperclip.copy("https://web.whatsapp.com")
    pyautogui.hotkey("ctrl", "v")
    pyautogui.press("enter")
    print("Opening WhatsApp Web...")
    time.sleep(15)  # Wait for WhatsApp to fully load


def send_message_to_number(phone, message):
    """Send message to a phone number via New Chat"""
    # Click New Chat button
    try:
         open_new_chat(phone)
         pyperclip.copy(message)
         pyautogui.hotkey("ctrl", "v")
         pyautogui.press("enter")
         print(f"Message sent to {phone}")
                        
    except Exception as e:
        print(f"Error opening chat for {phone}: {e}")
    #Send the message

    


def main():
    print("Starting WhatsApp automation in 5 seconds...")
    time.sleep(5)

    open_whatsapp()

    # Read numbers and messages from Excel
    df = pd.read_excel(EXCEL_FILE)

    for index, row in df.iterrows():
        name = str(row["Name"])
        phone = row["Phone"]
        message = "Welcome to the group, " + name + "! 🙏 Happy Learning!!"
        send_message_to_number(phone, message)
        time.sleep(3)  # Delay between messages

    print("All messages sent successfully!")


if __name__ == "__main__":
    main()