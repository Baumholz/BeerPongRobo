from distance import Distance
from engine import Engine
from time import sleep, sleep_us, sleep_ms
from light import Light
import utime
import time
from machine import Pin, PWM
import network
import socket
import urequests

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
turnOld = NO
countFront = 0
countRight = 0
countLeft = 0
countLight = ""
receive = 0

greenLightFront = False
greenLightRight = False
greenLightLeft = False
blueLightFront = False
blueLightRight = False
blueLightLeft = False
redLightFront = False
redLightRight = False
redLightLeft = False

def do_connect():
    import network
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect('WieHeistEuerWlan', 'Unser12PW34geht56so78')
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())

do_connect()

addr_info = socket.getaddrinfo("192.168.2.143", 42042)
addr = addr_info[0][-1]
s = socket.socket()
s.connect(addr)
s.send(b"CONNECTED")
print("Maybe sended")
#a = 0
try:
    engine.both()
    start = utime.ticks_us()
    t_last = time.time()
    timeE = 0
    while True:
        #print("Loops: " + str(a))
        #a += 1
        stop = utime.ticks_us()
        t = (stop-start)/1000000
        start = stop
        timeE += t        
        
        if receive == 0:
            countLight = ""
            countLight = s.recv(1024)
            print("received: " + str(countLight))
            if countLight == b'0' or countLight == b'1' or countLight == b'2':
                receive = 1
                print("RECEIVED SOMETIHNG!!" + " Receive = "+ str(receive))                                   
        tLED = time.time()
        if tLED-t_last > freq and countFront+countRight+countLeft < 3:                    
            print(LDRFront.value())
            if LDRFront.value() == 1 or countFront == 1:
                if redLightFront == False:
                    light.redLightFront()
                    greenLightFront = False
                    blueLightFront = False
                    redLightFront = True
                countFront = 1
                if countLight == b'0' and LDRFront.value() == 1:
                    countRight = 1
                    countLeft = 1
                    light.redLightRight()
                    light.redLightLeft()
                    receive = 0
            elif countLight == b'0' and countFront == 0:
                if blueLightFront == False:
                    light.blueLightFront()
                    blueLightFront = True
                    greenLightFront = False
                    redLightFront = False
            else:
                if greenLightFront == False:
                    light.greenLightFront()
                    blueLightFront = False
                    greenLightFront = True
                    redLightFront = False
                
            if LDRRight.value() == 1 or countRight == 1:
                if redLightRight == False:
                    light.redLightRight()
                    greenLightRight = False
                    blueLightRight = False
                    redLightRight = True
                countRight = 1
                if countLight == b'2' and LDRRight.value() == 1:
                    countFront = 1
                    countLeft = 1
                    light.redLightFront()
                    light.redLightLeft()
                    receive = 0
            elif countLight == b'2' and countRight == 0:
                if blueLightRight == False:
                    light.blueLightRight()
                    blueLightRight = True
                    greenLightRight = False
                    redLightRight = False
            else:
                if greenLightRight == False:
                    light.greenLightRight()
                    blueLightRight = False
                    greenLightRight = True
                    redLightRight = False
                
            if LDRLeft.value() == 1 or countLeft == 1:
                if redLightLeft == False:
                    light.redLightLeft()
                    redLightLeft = True
                    greenLightLeft = False
                    blueLightLeft = False
                countLeft = 1
                if countLight == b'1' and LDRLeft.value() == 1:
                    countFront = 1
                    countRight = 1
                    light.redLightFront()
                    light.redLightRight()
                    receive = 0
            elif countLight == b'1' and countLeft == 0:
                if blueLightLeft == False:
                    light.blueLightLeft()
                    redLightLeft = False
                    greenLightLeft = False
                    blueLightLeft = True                    
            else:
                if greenLightLeft == False:
                    light.greenLightLeft()
                    redLightLeft = False
                    greenLightLeft = True
                    blueLightLeft = False
            t_last = tLED
        elif countFront + countRight + countLeft == 3:
            light.bounce()
            engine.off()
            if tLED-t_last > 5*freq:
                countFront = 0
                countRight = 0
                countLeft = 0
                t_last = tLED
            
        try:
            left  = distance.get_left()
            right = distance.get_right()
        except OSError as exc:
            print(exc)
            
        # braun 4, gelb 5
        if timeE > .5:
            timeE = 0
            print("Left", "%6.2f" % left, "Right", "%6.2f" % right)
        
        turnOld = turn
        if turn == NO:                      
            if left > threshold:
                # links kante erkannt -> rechts drehen = links fahren
                #print("Turn right")
                turn = RIGHT
                #engine.left()
            elif right > threshold:
                # rechts kante erkannt -> links drehen = rechts fahren
                #print("Turn left")
                turn = LEFT
                #engine.right()
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
                #engine.both()              
        elif turn == RIGHT:           
            if left <= threshold:
                # stop
                #print("Walk")
                turn = NO
                #engine.both()  
        sleep(0.5)
        
        if turn != turnOld:
            if turn == LEFT:
                engine.right()
            if turn == RIGHT:
                engine.left()
            if turn == NO:
                engine.both()
        
except KeyboardInterrupt as e:
    print("off")
    engine.off()



