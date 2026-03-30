from flask import Flask, request, jsonify
import os
import subprocess
import time
import pyautogui

app = Flask(__name__)

#FILE_NAME = "socialeaglesri_demo.txt"

import os

FILE_NAME = r"C:\Users\SrividhyaGanesan\Documents\Sri\AI\socialeaglesri_demo.txt"

# Ensure directory exists
os.makedirs(r"C:\Users\SrividhyaGanesan\Documents\Sri\AI", exist_ok=True)

logs = []

def log(step):
    print(f"[DEBUG] {step}")
    logs.append(step)

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
    log("Closing Notepad...")
    pyautogui.hotkey("alt", "f4")
    time.sleep(1)
    log("Notepad closed.")

@app.route("/write", methods=["POST"])
def write_to_notepad():
    global logs
    logs = []

    data = request.get_json()

    if not data or "text" not in data:
        return jsonify({"error": "Missing 'text' in request body"}), 400

    user_text = data["text"]

    log("API request received")
    log(f"Input: {user_text}")

    # File check
    if not os.path.exists(FILE_NAME):
        log("File not found. Creating new file.")
        open(FILE_NAME, "w").close()
        log("File created.")
    else:
        log("File exists. Appending mode.")

    # Automation flow
    open_notepad(FILE_NAME)
    move_to_end_new_line()
    write_text(user_text)
    save_file()
    close_notepad()

    log("Process completed successfully.")

    return jsonify({
        "status": "success",
        "message": "Text written to Notepad",
        "logs": logs
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)