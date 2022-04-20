from consoles.sports import Basketball, Football, Swimming, Volleyball, WaterPolo, WaterPoloDaktronics
import time

if __name__ == '__main__':
    t = Swimming('/dev/ttyUSB0')
    print()
    while True:
        time.sleep(0.025)
        # print(t.export(), end='\r')
        data = t.export()
        event = data['event']
        heat = data['heat']
        rtime = data['time']
        length = data['lengths']
        la = data['2']
        lb = data['3']
        lc = data['4']
        print(f'E{event} H{heat} T {rtime} ({length})- LA {la} - LB {lb} - LC {lc}')
        # print(data['time'],end='\r')
