from distance import Distance
from engine import Engine
from time import sleep, sleep_us, sleep_ms
import utime

engine = Engine()
distance = Distance()

threshold = 20

NO = 0
LEFT = 1
RIGHT = 2
turn = NO

try:
    engine.both()
    start = utime.ticks_us()
    time = 0
    while True:
        stop = utime.ticks_us()
        t = (stop-start)/1000000
        start = stop
        time += t
        
            
        left  = distance.get_left()
        right = distance.get_right()
        
        # braun 4, gelb 5
        if time > .5:
            time = 0
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
                print("pass")
                pass
                #engine.both()          
        elif turn == LEFT:
            if right <= threshold:
                # stop
                print("Walk")
                turn = NO
                engine.both()              
        elif turn == RIGHT:           
            if left <= threshold:
                # stop
                print("Walk")
                turn = NO
                engine.both()  
        #sleep(0.1)
        
except KeyboardInterrupt as e:
    print("off")
    engine.off()

