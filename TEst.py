import time

freq = 1
t_last = time.time()

while True:
    t = time.time()
    if t-t_last > freq:
        print(str(t) + " "+ str(t_last))
        t_last = t