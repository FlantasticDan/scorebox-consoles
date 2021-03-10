from consoles.sports import Volleyball, WaterPolo
import time

t = WaterPolo('COM6')
while True:
    time.sleep(1)
    print(t.export())