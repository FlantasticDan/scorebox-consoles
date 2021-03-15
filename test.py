from consoles.sports import Basketball, Football, Volleyball, WaterPolo, WaterPoloDaktronics
import time

if __name__ == '__main__':
    t = WaterPolo('COM6')
    print()
    while True:
        time.sleep(0.1)
        print(t.export(), end='\r')
