import pyautogui
import time

print("hello")
# Mouse Operations
print("Click")
pyautogui.click(200,100)
time.sleep(2)
print("Right Click")
pyautogui.rightClick(200,500)
time.sleep(10)
print("Find coordinates of click")
x,y=pyautogui.position()
print("Coordinates of click: ",x,y)
time.sleep(2)
#print("Move mouse to specific coordinates")
pyautogui.click(1483, 463)



