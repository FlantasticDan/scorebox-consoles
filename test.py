from consoles.sports import Volleyball, WaterPolo
import time

if __name__ == '__main__':
    t = Volleyball('COM4')
    print()
    while True:
        time.sleep(0.1)
        print(t.export(), end='\r')
