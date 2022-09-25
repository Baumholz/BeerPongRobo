import machine, neopixel, time
from time import sleep, sleep_us, sleep_ms

n=8

right = neopixel.NeoPixel(machine.Pin(5), n)
front = neopixel.NeoPixel(machine.Pin(18), n)
left = neopixel.NeoPixel(machine.Pin(19), n)

def greenLight():
    #bounce(0,128,0,front)
    for i in range(n):
        right[i] = (0, 128, 0)
        front[i] = (0, 128, 0)
        left[i] = (0, 128, 0)
        right.write()
        front.write()
        left.write()
        
        
def redLight():
    for i in range(n):
        right[i] = (255, 0, 0)
        front[i] = (255, 0, 0)
        left[i] = (255, 0, 0)
        right.write()
        front.write()
        left.write()
        
def bounce(r, g, b, light):
    for i in range(4 * n):
        for j in range(n):
            light[j] = (r, g, b)
        if (i // n) % 2 == 0:
            light[i % n] = (0, 0, 0)
        else:
            tmp =  n–1–(i % n)
            light[tmp] = (0, 0, 0)
        light.write()

while True:
    redLight()
    sleep(5)
    greenLight()
    sleep(5)