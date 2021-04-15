from consoles.sports import Basketball, Football, Swimming, Volleyball, WaterPolo, WaterPoloDaktronics
import time

if __name__ == '__main__':
    t = Swimming('COM6')
    print()
    while True:
        time.sleep(1)
        # print(t.export(), end='\r')
        data = t.export()
        event = data['event']
        heat = data['heat']
        l2 = data['2']
        l3 = data['3']
        l4 = data['4']
        print(f'E{event} H{heat} - L2 {l2} - L3 {l3} - L4 {l4}')
