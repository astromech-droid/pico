from Leds import LEDS
from Time import Time

time = Time()
leds = LEDS()

leds.enable_blink(interval=300)

while True:
    leds.display(time.get())
    
    if time.is_commited():
        leds.disable_blink()