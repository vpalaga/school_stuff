import machine
from ws2812 import WS2812
import utime
import urandom

# Number of LEDs in the strip
NUM_LEDS = 8

# Initialize the LED strip with 8 LEDs
led_strip = WS2812(machine.Pin(0), NUM_LEDS)

def flowing_light():
    # Shift colors along the strip
    for i in range(NUM_LEDS - 1, 0, -1):
        led_strip[i] = led_strip[i - 1]
    # Generate a random color for the first LED
    led_strip[0] = [urandom.getrandbits(8), urandom.getrandbits(8), urandom.getrandbits(8)]
    # Update the strip
    led_strip.write()
    # Small delay for smooth animation
    utime.sleep_ms(100)

# Main loop
while True:
    flowing_light()