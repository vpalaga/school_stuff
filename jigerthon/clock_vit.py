from gturtle import *
from datetime import datetime
import time
makeTurtle()
hideTurtle()

def clock(radius, th_l, sm_l, th_w, sm_w):
    clear()
    heading(0)
    setPos(0, 0)
    spc("black")
    
    for hour in range(12):
        
        for minute in range(5):
            penUp()
            if minute == 0:  #
                fd(radius-th_l)
                penDown()
                spw(th_w)
                fd(th_l)
            else:
                fd(radius - sm_l)
                penDown()
                spw(sm_w)
                fd(sm_l)
                
            setPos(0, 0)
            rt(6)
    
    
    now = datetime.now()
    
    heading(360/12*now.hour)
    spw(th_w)
    fd(radius * 3 / 5)
    
    setPos(0, 0)
    heading(360/60*now.minute)
    spw(sm_w)
    fd(radius * 3 / 4)
    
    setPos(0, 0)
    heading(360/60*now.second)
    spc("red")
    fd(radius * 4 / 5)
    

while True:        
    clock(270, 30, 10, 15, 3)
    time.sleep(1)