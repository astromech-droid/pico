from machine import Pin, Timer
from time import sleep

class LEDS:
    digits = [
        Pin(16, Pin.OUT),
        Pin(17, Pin.OUT),
        Pin(18, Pin.OUT),
        Pin(19, Pin.OUT)
    ]

    segments = [
        Pin(2, Pin.OUT),  # A
        Pin(3, Pin.OUT),  # B
        Pin(6, Pin.OUT),  # C
        Pin(7, Pin.OUT),  # D
        Pin(10, Pin.OUT), # E
        Pin(11, Pin.OUT), # F
        Pin(14, Pin.OUT), # G
    ]

    patterns = [
        #A,B,C,D,E,F,G
        [1,1,1,1,1,1,0], # 0
        [0,1,1,0,0,0,0], # 1
        [1,1,0,1,1,0,1], # 2
        [1,1,1,1,0,0,1], # 3
        [0,1,1,0,0,1,1], # 4
        [1,0,1,1,0,1,1], # 5
        [1,0,1,1,1,1,1], # 6
        [1,1,1,0,0,0,0], # 7
        [1,1,1,1,1,1,1], # 8
        [1,1,1,1,0,1,1], # 9
    ]
    
    visible = True
    blink = False
    timer = Timer()
    refresh_interval = 0.008 # これより長いとチカチカし、短いと数字が混ざる
    

    # 概要: 一桁だけ数字を点灯する
    # 引数: 何桁目に何の数字を点灯するか
    def turn_on(self, digit:int, num:int):
        self.digits[digit].high()
        others = self.digits[:digit] + self.digits[digit+1:]
    
        for o in others:
            o.low()
    
        for idx, value in enumerate(self.patterns[num]):
            if value == 1:
                self.segments[idx].low()
            elif value == 0:
                self.segments[idx].high()


    # 概要: 全桁消灯する
    def turn_off(self):
        for i in range(4):
            self.digits[i].low()    


    # 概要: 動作を開始する
    def display(self, time:list):
        if self.visible:
            # 全桁点灯しているように見せる
            for i in range(4):
                self.turn_on(i, time[i])
                sleep(self.refresh_interval)
            
        else:
            # 全桁消灯する
            self.turn_off()
    
    
    # 概要: 一定間隔でLEDを点滅させる
    # 引数: 点滅の間隔
    def enable_blink(self, interval:int):
        def _toggle(timer):
            self.visible = not self.visible
        
        if not self.blink:
            self.timer.init(period=interval, callback=_toggle)
        
        self.blink = True


    # 概要: 点滅を停止する
    def disable_blink(self):
        if self.blink:
            self.timer.deinit()
            self.blink = False
            self.visible = True