import pyautogui
import pyperclip
import time
import sys

# Safety: move mouse to top-left corner to abort
pyautogui.FAILSAFE = True

def open_browser():
    try:
        # Open Run dialog (Windows)
        pyautogui.hotkey('win', 'r')
        time.sleep(1)

        # Type chrome (change to 'msedge' if using Edge)
        pyautogui.write('msedge', interval=0.1)
        pyautogui.press('enter')

        time.sleep(5)  # Wait for browser to open

    except Exception as e:
        print("Error opening browser:", e)
        sys.exit()


def search_gold_rate():
    try:
        query = "today's gold rate in chennai"

        # Focus address bar
        pyautogui.hotkey('ctrl', 'l')
        time.sleep(1)

        # Copy query safely
        pyperclip.copy(query)

        # Paste query
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(1)

        pyautogui.press('enter')
        time.sleep(5)  # Wait for results to load

    except Exception as e:
        print("Error during search:", e)
        sys.exit()


def click_first_link():
    try:
        # Press Tab a few times to reach first search result
        for _ in range(5):
            pyautogui.press('tab')
            time.sleep(0.5)

        pyautogui.press('enter')
        print("Clicked first link successfully!")

    except Exception as e:
        print("Error clicking first link:", e)
        sys.exit()


def main():
    print("Starting automation in 3 seconds...")
    time.sleep(3)

    open_browser()
    search_gold_rate()
    click_first_link()

    print("Task completed successfully!")


if __name__ == "__main__":
    main()