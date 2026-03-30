import os
import sys
import subprocess
import time
import pyautogui

FILE_NAME = "socialeaglesri_demo.txt"

def log(step):
    print(f"[DEBUG] {step}")

def open_notepad(file_path):
    log("Opening Notepad...")
    subprocess.Popen(["notepad.exe", file_path])
    time.sleep(2)
    log("Notepad opened.")

def move_to_end_new_line():
    log("Moving cursor to end of file...")
    pyautogui.hotkey("ctrl", "end")
    time.sleep(0.5)

    log("Adding new line...")
    pyautogui.press("enter")
    time.sleep(0.5)

def write_text(text):
    log(f"Writing text: {text}")
    pyautogui.write(text, interval=0.05)
    log("Text written.")

def save_file():
    log("Saving file (Ctrl + S)...")
    pyautogui.hotkey("ctrl", "s")
    time.sleep(1)
    log("File saved.")

def close_notepad():
    log("Closing Notepad (Alt + F4)...")
    pyautogui.hotkey("alt", "f4")
    time.sleep(1)
    log("Notepad closed.")

def main():
    log("Script started.")

    if len(sys.argv) < 2:
        log("ERROR: No input provided.")
        print("Usage: python script.py <text>")
        sys.exit(1)

    user_text = " ".join(sys.argv[1:])
    log(f"Input received: {user_text}")

    if not os.path.exists(FILE_NAME):
        log("File not found. Creating new file.")
        open(FILE_NAME, "w").close()
        log("File created.")
    else:
        log("File exists. Appending mode.")

    open_notepad(FILE_NAME)

    move_to_end_new_line()
    write_text(user_text)

    save_file()
    close_notepad()

    log("Process completed successfully.")

if __name__ == "__main__":
    main()