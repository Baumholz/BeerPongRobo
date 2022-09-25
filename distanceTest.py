from distance import Distance
from time import sleep

distance = Distance()

while True:
    left  = distance.get_left()
    right = distance.get_right()
    
    print("Left", "%6.2f" % left, "Right", "%6.2f" % right)
    sleep(0.5)
