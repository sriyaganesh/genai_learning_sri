import pyautogui
import time

def find_coordinates():
    print("Find coordinates of click")
    x, y = pyautogui.position()
    print("Coordinates of click: ", x, y)
    return x, y

if __name__ == "__main__":
    print("Click on the screen to find the coordinates...")
    time.sleep(5)  # Wait for 5 seconds to allow user to click
    find_coordinates()