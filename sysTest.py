import network
import socket
import urequests
from time import sleep

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
while True:
    data = ""
    data = s.recv(1024)
    print(data)
    sleep(2)


#response = urequests.post("192.168.2.143", data = "b"CONNECTED"")
