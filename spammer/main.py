import pyautogui as pg
import time
import keyboard  # pip install keyboard

def action():
    pg.typewrite("67", interval=0)
    pg.press("enter")

    time.sleep(0.01)

time.sleep(5)
while True:
    action()

    # check if 'c' is pressed
    if keyboard.is_pressed("p"):
        print("You pressed p. Stopping.")
        break