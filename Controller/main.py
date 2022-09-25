import network
import socket
import urequests
from time import sleep
import utime
from machine import Pin, ADC
import neopixel

n=24
xAxis = ADC(0)
yAxis = Pin(12, Pin.IN)
SW = Pin(14,Pin.IN, Pin.PULL_UP)
readDelay = 0.5
light = neopixel.NeoPixel(machine.Pin(5), n)
count = 0

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

addr_info = socket.getaddrinfo("192.168.2.143", 42069)
addr = addr_info[0][-1]
s = socket.socket()
s.connect(addr)
s.send(b"CONNECTED")
print("Maybe sended")

for i in range(n):
            light[i] = (0, 128, 0)
            light.write()

while True:
    
    xRef = xAxis.read_u16()
    #yRef = yAxis.read_u16()
    
    #yRef = yAxis.value()
    xRef = xAxis.read()
    SWPushed= SW.value()
    print("X: " + str(xRef) + ", SW: " + str(SWPushed))
    
    if xRef <= 100:
        count = count + 1
        if count == 3:
            count = 0
    elif xRef >= 1000:
        count = count -1
        if count == -1:
            count = 2
    
    if count == 1:
        x = 0
        while x < 8:
            light[x] = (0,0,255)
            light[x+8] = (0, 128, 0)
            light[x+16] = (0, 128, 0)
            light.write()
            x += 1
    elif count == 2:
        x = 8
        while x < 16:
            light[x] = (0,0,255)
            light[x+8] = (0, 128, 0)
            light[x-8] = (0, 128, 0)
            light.write()
            x += 1
    elif count == 0:
        x = 16
        while x < 24:
            light[x] = (0,0,255)
            light[x-8] = (0, 128, 0)
            light[x-16] = (0, 128, 0)
            light.write()
            x += 1
            
    if SWPushed == 0:
        s.send(str(count))
        print("Sended: "+str(count))
              
    sleep(0.5)