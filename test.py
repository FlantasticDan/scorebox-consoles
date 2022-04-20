from consoles.sports import Basketball, Football, Swimming, Volleyball, WaterPolo, WaterPoloDaktronics
import time

if __name__ == '__main__':
    t = Swimming('/dev/ttyUSB0')
    print()
    while True:
        time.sleep(0.05)
        # print(t.export(), end='\r')
        data = t.export()
        event = data['event']
        heat = data['heat']
        la = data['1']
        lb = data['3']
        lc = data['5']
        print(f'E{event} H{heat} - LA {la} - LB {lb} - LC {lc}')
        # print(data['running_time'],end='\r')
