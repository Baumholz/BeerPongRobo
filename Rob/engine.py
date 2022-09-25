from machine import Pin, PWM
from time import sleep

class Engine():
    def __init__(self):
        self.right_weel_right_pin = Pin(12, Pin.OUT)
        self.right_weel_left_pin = Pin(14, Pin.OUT)
        self.left_weel_right_pin = Pin(26, Pin.OUT)
        self.left_weel_left_pin = Pin(27, Pin.OUT)
        self.test = Pin(5, Pin.OUT)
        
    def left(self):
        self.left_weel_right_pin.on()
        self.test.on()
        self.left_weel_left_pin.off()
        
        self.right_weel_right_pin.off()
        self.right_weel_left_pin.on()        
        
    def right(self):
        self.left_weel_right_pin.off()
        self.test.off()
        self.left_weel_left_pin.on()
        
        self.right_weel_right_pin.on()
        self.right_weel_left_pin.off()       
    
    def both(self):
        self.left_weel_right_pin.on()
        self.test.on()
        self.left_weel_left_pin.off()
        
        self.right_weel_right_pin.on()
        self.right_weel_left_pin.off()
    
    def off(self):
        self.left_weel_right_pin.off()
        self.left_weel_left_pin.off()
        self.right_weel_right_pin.off()
        self.right_weel_left_pin.off()
        self.test.off()

if __name__ == "__main__":
    try:
        engine = Engine()
        while True:
            print("Left")
            engine.left()
            sleep(2)
            print("Right")
            engine.right()
            sleep(2)
            print("Both")
            engine.both()
            sleep(2)
            print("Off")
            engine.off()
            sleep(2)
    except Exception as e:
        print(e)

    engine.off()

