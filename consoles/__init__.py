import serial
from threading import Thread

class SerialConnection:
    '''Low Level Serial Connection to Scoreboard.'''
    def __init__(self, port: str, baudrate: int, parity) -> None:
        self.connection = serial.Serial(port=port, baudrate=baudrate, parity=parity, timeout=0)

        self.thread = None # Thread()
    
    def runner(self) -> None:
        self.thread = Thread(target=self.run)
        self.thread.start()

    def run(self) -> None:
        self.update()
    
    def update(self) -> None:
        '''Re-implement as a loop to process and reieve data from the serial connection.'''
        raise AssertionError("method `update` must be reimplemented")