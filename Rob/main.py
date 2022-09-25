from distance import Distance
from engine import Engine
from time import sleep, sleep_us, sleep_ms
from light import Light
import utime
import time
from machine import Pin, PWM

LDRFront = Pin(16, Pin.IN)
LDRRight = Pin(17, Pin.IN)
LDRLeft = Pin(4, Pin.IN)

engine = Engine()
distance = Distance()
light = Light()

threshold = 20
freq = 1

NO = 0
LEFT = 1
RIGHT = 2
turn = NO
countFront = 0
countRight = 0
countLeft = 0
countLight = ""

try:
    engine.both()
    start = utime.ticks_us()
    t_last = time.time()
    timeE = 0
    while True:
        stop = utime.ticks_us()
        t = (stop-start)/1000000
        start = stop
        timeE += t
        
        tLED = time.time()
        if tLED-t_last > freq and countFront+countRight+countLeft < 3:                    
            print(LDRFront.value())
            if LDRFront.value() == 1 or countFront == 1:
                light.redLightFront()
                countFront = 1
                if countLight == b'0':
                    countRight = 1
                    countLeft = 1
                    light.redLightRight()
                    light.redLightLeft()
            else:
                light.greenLightFront()
                
            if LDRRight.value() == 1 or countRight == 1:
                light.redLightRight()
                print("LED RIGH REDLIGHT!")
                countRight = 1
                if countLight == b'2':
                    countFront = 1
                    countLeft = 1
                    light.redLightFront()
                    light.redLightLeft()
            else:
                light.greenLightRight()
                
            if LDRLeft.value() == 1 or countLeft == 1:
                light.redLightLeft()
                countLeft = 1
                if countLight == b'1':
                    countFront = 1
                    countLeft = 1
                    light.redLightFront()
                    light.redLightRight()
            else:
                light.greenLightLeft()
            t_last = tLED
        elif countFront + countRight + countLeft == 3:
            light.bounce()
            if tLED-t_last > 5*freq:
                countFront = 0
                countRight = 0
                countLeft = 0
                t_last = tLED
            
            
        left  = distance.get_left()
        right = distance.get_right()
        
        # braun 4, gelb 5
        if timeE > .5:
            timeE = 0
            print("Left", "%6.2f" % left, "Right", "%6.2f" % right)
        
        if turn == NO:                      
            if left > threshold:
                # links kante erkannt -> rechts drehen = links fahren
                print("Turn right")
                turn = RIGHT
                engine.left()
            elif right > threshold:
                # rechts kante erkannt -> links drehen = rechts fahren
                print("Turn left")
                turn = LEFT
                engine.right()
            else:
                # laufe bis kante
                #print("pass")
                pass
                #engine.both()          
        elif turn == LEFT:
            if right <= threshold:
                # stop
                #print("Walk")
                turn = NO
                engine.both()              
        elif turn == RIGHT:           
            if left <= threshold:
                # stop
                #print("Walk")
                turn = NO
                engine.both()  
        #sleep(0.1)
        
except KeyboardInterrupt as e:
    print("off")
    engine.off()

