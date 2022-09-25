import machine, neopixel, time
from machine import Pin, PWM

n=8

class Light:
    def __init__(self):
        self.right = neopixel.NeoPixel(machine.Pin(5), n)
        self.front = neopixel.NeoPixel(machine.Pin(18), n)
        self.left = neopixel.NeoPixel(machine.Pin(19), n)
    
    def greenLightFront(self):
        #bounce(0,128,0,front)
        for i in range(n):
            self.front[i] = (0, 128, 0)
            self.front.write()
        
    def greenLightRight(self):
        for i in range(n):
            self.right[i] = (0, 128, 0)
            self.right.write()
        
    def greenLightLeft(self):
        for i in range(n):
            self.left[i] = (0, 128, 0)
            self.left.write()
    
    def redLightFront(self):
        for i in range(n):
            self.front[i] = (255, 0, 0)
            self.front.write()

    def redLightRight(self):
        for i in range(n):
            self.right[i] = (255, 0, 0)
            self.right.write()
    
    def redLightLeft(self):
        for i in range(n):
            self.left[i] = (255, 0, 0)
            self.left.write()
        
    def bounce(self):
         for i in range(4 * n):
            for j in range(n):
                self.front[j] = (0, 0, 255)
                self.right[j] = (0, 0, 255)
                self.left[j] = (0, 0, 255)
            self.front[i % n] = (255, 0, 0)
            self.right[i % n] = (0, 255, 0)
            self.left[i % n] = (255, 250, 0)
            self.front.write()
            self.right.write()
            self.left.write()
            time.sleep_ms(100)