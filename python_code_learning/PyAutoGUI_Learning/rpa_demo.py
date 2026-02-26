import pyautogui
import time

print("hello")
# Mouse Operations
print("Click")
pyautogui.click(200,100)
time.sleep(2)
print("Right Click")
pyautogui.rightClick(200,500)
time.sleep(4)


time.sleep(2)
#print("Move mouse to specific coordinates")
pyautogui.click(1483, 463)

pyautogui.doubleClick(1483, 463)
time.sleep(2)

# Scroll Functions
print("Scrolling Up")
pyautogui.scroll(5)  # Positive number = scroll up
time.sleep(1)

print("Scrolling Down")
pyautogui.scroll(-5)  # Negative number = scroll down
time.sleep(1)

# Scroll at specific coordinates
print("Scrolling up at specific location")
pyautogui.scroll(10, x=500, y=300)  # Scroll up at coordinates (500, 300)
time.sleep(1)

print("Scrolling down at specific location")
pyautogui.scroll(-10, x=500, y=300)  # Scroll down at coordinates (500, 300)
time.sleep(2)

#pyautogui.drag(500,500,1000,1000)
#pyautogui.dragfrom(500,500,1000,1000)
pyautogui.dragTo(300,500, duration=1)



