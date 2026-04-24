import subprocess
import time
import pyautogui

# Path to GlobalProtect
gp_path = r"C:\Program Files\Palo Alto Networks\GlobalProtect\PanGPA.exe"

# Launch app
subprocess.Popen(gp_path)

# Wait for UI to appear
time.sleep(5)

pyautogui.moveTo(1771, 1096, duration=0.5)
pyautogui.click()
print("Connect button clicked")
