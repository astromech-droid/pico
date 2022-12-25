import time
from machine import Pin, Timer, RTC

rtc = RTC()
timestamp= [8, 8, 8, 8]

# これより遅いとチカチカする。速いと他の数字と混ざる
refresh_interval = 0.008

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

uc_lc = Pin(15, Pin.OUT)
led = Pin(25, Pin.OUT)

buttons = [
    Pin(20, Pin.IN, Pin.PULL_DOWN),
    Pin(21, Pin.IN, Pin.PULL_DOWN),
    Pin(22, Pin.IN, Pin.PULL_DOWN),
    Pin(26, Pin.IN, Pin.PULL_DOWN),
    Pin(27, Pin.IN, Pin.PULL_DOWN)
]

seg_ptn = [
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


# LEDを数字の形に設定する
def set_number(num:int):
    for idx,sp in enumerate(seg_ptn[num]):
        if sp == 0:
            segments[idx].value(1)
        elif sp == 1:
            segments[idx].value(0)


# 指定された桁のLEDのみ点灯する
def turn_leds_on(digit_num:int):    
    active = digits[digit_num]
    active.value(1)

    inactive = digits[:digit_num] + digits[digit_num+1:]

    for i in inactive:
        i.value(0)


def zfill(number:int) -> str:
    if number <= 9:
        return "0" + str(number)
    else:
        return str(number)


def read_time(timer):
    now:tuple = rtc.datetime()[4:6]
    hours:str = zfill(now[0])
    minutes:str = zfill(now[1])
    
    timestamp[0] = int(hours[0])
    timestamp[1] = int(hours[1])
    timestamp[2] = int(minutes[0])
    timestamp[3] = int(minutes[1])
    
    # 秒針をLEDで表現
    led.toggle()


def main():
    timer = Timer()
    timer.init(period=1000, callback=read_time)
    
    # 真ん中のコロンは常に点灯
    uc_lc.value(0)
    
    while True:   
        for i in range(4):
            
            if i == 0:
                set_number(timestamp[0])
            elif i == 1:
                set_number(timestamp[1])
            elif i == 2:
                set_number(timestamp[2])
            elif i == 3:
                set_number(timestamp[3])
        
            turn_leds_on(i)
            time.sleep(refresh_interval)

main()
