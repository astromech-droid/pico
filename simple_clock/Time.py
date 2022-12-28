from machine import Pin, RTC, Timer
from time import ticks_ms, ticks_diff
from math import floor

class Time:
    time = [0] * 4

    buttons = [
        Pin(20, Pin.IN, Pin.PULL_DOWN),
        Pin(21, Pin.IN, Pin.PULL_DOWN),
        Pin(22, Pin.IN, Pin.PULL_DOWN),
        Pin(26, Pin.IN, Pin.PULL_DOWN),
        Pin(27, Pin.IN, Pin.PULL_DOWN)
    ]
    
    ticks = ticks_ms()
    commited = False
    rtc = RTC()
    timer = Timer()

    def __init__(self, second_hand:Pin):
        self.second_hand = second_hand
        
        def _count_up(pin):
            # チャタリング対策                  
            if ticks_diff(ticks_ms(), self.ticks) > 150:
                idx = self.buttons.index(pin)
            
                if self.time[idx] >= 9:
                    self.time[idx] = 0
                    
                else:
                    self.time[idx] += 1
    
            self.ticks = ticks_ms()
        
        def _commit(pin):
            if int(str("").join([str(n) for n in self.time])) <= 2359:
                hours = self.time[0] * 10 + self.time[1]
                minutes = self.time[2] * 10 + self.time[3]
                self.rtc.datetime((1993, 10, 18, 0, hours, minutes, 0, 0))
                self.sync_rtc()
                self.commited = True
                
            else:
                pass
        
        for i in range(5):
            if i <= 3:
                self.buttons[i].irq(handler=_count_up, trigger=Pin.IRQ_RISING)
            if i == 4:
                self.buttons[i].irq(handler=_commit, trigger=Pin.IRQ_RISING)


    def sync_rtc(self):
        def _sync(timer):
            self.second_hand.high()

            hours, minutes = self.rtc.datetime()[4:6]
            self.time[0] = floor(hours / 10)
            self.time[1] = hours - self.time[0] * 10
            self.time[2] = floor(minutes / 10)
            self.time[3] = minutes - self.time[2] * 10

            self.second_hand.low()

        self.timer.init(period=1000, callback=_sync)


    def get(self):
        return self.time
    

    def is_commited(self):
        return self.commited