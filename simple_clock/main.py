from Leds import LEDS
from Time import Time
from machine import Pin

time = Time(second_hand=Pin(25, Pin.OUT))
leds = LEDS()

leds.enable_blink(interval=300)

while True:
    leds.display(time.get())
    
    if time.is_commited():
        leds.disable_blink()