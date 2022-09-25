import utime
from machine import Pin, PWM
#IMPORTANT! HC-SR04 runs on 5V; Connect its VCC to VBUS (pin 40)
from collections import namedtuple

class Distance:
    def __init__(self):
        DistanceSensor = namedtuple("DistanceSensor", ["echo", "trigger"])

        self.left  = DistanceSensor(echo=Pin(35, Pin.IN), trigger=Pin(32, Pin.OUT))
        self.right = DistanceSensor(echo=Pin(33, Pin.IN), trigger=Pin(25, Pin.OUT))
    
    def get_distance(self, obj):
        obj.trigger.off()
        utime.sleep_us(2)
        obj.trigger.on()
        utime.sleep_us(5)
        obj.trigger.off()
        #signaloff = utime.ticks_us()
        print("Wait for 0")
        while obj.echo.value() == 0:
            signaloff = utime.ticks_us()
        #signalon = utime.ticks_us()
        print("Wait for 1")
        while obj.echo.value() == 1:
            signalon = utime.ticks_us()
        timepassed = signalon - signaloff
        distance = (timepassed * 0.0343) / 2
        #print("The distance from object is ", distance, "cm")
        return distance
    
    def get_left(self):
        return self.get_distance(self.left)
    
    def get_right(self):
        return self.get_distance(self.right)

