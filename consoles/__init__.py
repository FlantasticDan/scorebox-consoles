from multiprocessing.connection import Connection
from typing import Dict
import serial
from threading import Thread
from multiprocessing import Process, Pipe, freeze_support

class SerialConnection:
    '''Low Level Serial Connection to Scoreboard.'''
    def __init__(self, port: str, baudrate: int, parity) -> None:
        self.port = port
        self.baudrate = baudrate
        self.parity = parity

        # Data stores the raw structured result of incoming scoreboard console serial data.
        self.data = {}

        self.reciever, self.sender = Pipe(False)
        self.serial_process = None # Process
        self.update_thread = None # Thread

    def runner(self) -> None:
        self.serial_process = Process(target=self.run, args=(self.sender, self.port, self.baudrate, self.parity,))
        self.serial_process.start()

        self.update_thread = Thread(target=self.updater, args=(self.reciever,))
        self.update_thread.start()

    def run(self, send_pipe: Connection, port: str, baudrate: int, parity) -> None:
        '''Entrypoint for the Serial Update Process, runs as a seperate process.'''
        connection = serial.Serial(port=port, baudrate=baudrate, parity=parity, timeout=0)
        self.update(send_pipe, connection)
    
    def updater(self, recv_pipe: Connection) -> None:
        '''Updater running in it's own thread recieving data updates from the serial update process.'''
        while True:
            self.data = recv_pipe.recv()
            self.on_update(self.data)

    def on_update(self, data: Dict) -> None:
        '''Optionally re-implement to run each time new data is processed from the score console.'''
        pass

    def update(self, send_pipe: Connection, connection: serial.Serial) -> None:
        '''Re-implement as a loop to process and reieve data from the serial connection.'''
        raise AssertionError("method `update` must be reimplemented")