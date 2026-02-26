import pyautogui
import pyperclip
import time
from urllib.parse import quote

pyautogui.FAILSAFE = True  # Move mouse to top-left to stop script

# Contact and message
CONTACT_NAME = "my family"
MESSAGE = "Om Sai Ram 🙏 Have a blessed day!"

# Images
NEW_CHAT_IMG = "new_chat.png"
SEARCH_BAR_IMG = "search_icon.png"

# Retry settings
MAX_RETRIES = 10
CONFIDENCE = 0.6
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

# Step 1: Open WhatsApp Web
def open_whatsapp():
    pyautogui.hotkey("win", "r")
    time.sleep(1)
    pyautogui.write("msedge")  # Open Microsoft Edge
    pyautogui.press("enter")
    time.sleep(5)
    pyautogui.hotkey("ctrl", "l")
    pyperclip.copy("https://web.whatsapp.com")
    pyautogui.hotkey("ctrl", "v")
    pyautogui.press("enter")
    print("Opening WhatsApp Web...")
    time.sleep(15)  # Wait for page to load

# Step 2: Create New Chat and Search Contact
def open_new_chat(contact_name):
    if not locate_and_click(NEW_CHAT_IMG, "New Chat button"):
        return False

    # if not locate_and_click(SEARCH_BAR_IMG, "Search bar"):
    #     return False

    pyperclip.copy(contact_name)
    pyautogui.hotkey("ctrl", "v")
    time.sleep(2)
    pyautogui.press("enter")
    time.sleep(2)
    print(f"Opened chat with {contact_name}")
    return True

# Step 3: Send Message
def send_message(message):
    pyperclip.copy(message)
    pyautogui.hotkey("ctrl", "v")
    pyautogui.press("enter")
    print("Message sent successfully!")

# Main function
def main():
    print("Starting automation in 5 seconds...")
    time.sleep(5)
    open_whatsapp()
    if open_new_chat(CONTACT_NAME):
        send_message(MESSAGE)
    print("Task completed.")

if __name__ == "__main__":
    main()