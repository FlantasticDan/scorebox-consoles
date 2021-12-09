from consoles.sports import Basketball, Football, Volleyball, WaterPolo, WaterPoloDaktronics, Wrestling
import time

if __name__ == '__main__':
    t = Wrestling('COM9')
    print()
    while True:
        time.sleep(0.1)
        print(t.export(), end='\r')
