from machine import Pin
from utime import sleep

pin = Pin(16, Pin.OUT)

print("LED starts flashing...")
sleep_time = 1

while True:
    try:
        pin.toggle()
        sleep(sleep_time) # sleep 1sec
    except KeyboardInterrupt:
        break

pin.off()
print("Finished.")
