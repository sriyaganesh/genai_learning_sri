import pyautogui
import time

# Keyboard Operations
print("Keyboard Operations ")
#time.sleep(2)
#pyautogui.write("Hello, This is a test of PyAutoGUI for keyboard operations.")
#time.sleep(2)
# x, y = pyautogui.position()
# print("Coordinates of click: ", x, y)
# Click and write at specific coordinates
# pyautogui.click(795,461)
# pyautogui.write("#This is a PyAutoGUI demo to write at a specific location.")
# pyautogui.press('enter')


# pyautogui.write("#This is the second line of text.")
# pyautogui.press('enter')

# pyautogui.write("pyautogui test")
# pyautogui.press('enter')cd 
#pyautogui.hotkey('ctrl','a')
time.sleep(2)
#pyautogui.click(pyautogui.center(location))
from PIL import Image
#Image.open("D:\Sri\GenAI\genai_learning_sri\python_code_learning\PyAutoGUI_Learning\copilot_img.png").show()
image_path = r"D:\Sri\GenAI\genai_learning_sri\python_code_learning\PyAutoGUI_Learning\copilot_image.png"


# region = (100, 100, 200, 200)  # x, y, width, height

# pyautogui.screenshot("copilot_img.png", region=region)
location =  pyautogui.locateOnScreen(image_path, confidence=0.8)
print(location)
pyautogui.click(pyautogui.center(location))
print(pyautogui.size())
f=pyautogui.screenshot()
f.save("demo_screenshot.png")


