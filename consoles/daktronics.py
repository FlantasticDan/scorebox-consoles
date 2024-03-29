from typing import Tuple
import serial
from serial import PARITY_NONE
from serial.serialutil import SerialException 
from multiprocessing.connection import Connection

from . import SerialConnection

class Daktronics (SerialConnection):
    '''Daktronics Serial Connection Controller.'''
    def __init__(self, port: str) -> None:
        super().__init__(port, 19200, PARITY_NONE)
    
    def process(self, message: str, message_range: Tuple[int, int]) -> None:
        '''Re-implement as the sport's Real Time Data processor'''
        raise AssertionError('method `process` must be reimplemented for each sport.')

    def parse(self, message: str) -> None:
        '''Parse Daktronics Real Time Data'''

        try:
            header, unprocessed = message.split(chr(2))
            text, checksum = unprocessed.split(chr(4))
            start = int(header[-4] + header[-3] + header[-2] + header[-1]) + 1
            end = start + len(text) - 1
            self.process(text, (start, end))
        except ValueError:
            pass

    def get_field(self, text: str, message_range: Tuple[int, int], item: int, length: int) -> str:
        if message_range[0] <= item <= message_range[1]:
            return text[item - message_range[0]: item + length - message_range[0]]
        return ''

    def update(self, send_pipe: Connection, connection: serial.Serial) -> None:
        while True:
            send_pipe.send(self.data)
            # Filter out 'SYNC IDLE' transmissions
            control_character = 0
            while control_character != b'\x16':
                try:
                    control_character = connection.read()
                except SerialException:
                    continue
            message = ''
            last_character = b''
            # Real Time Data Messages end with a 'END TRANSMISSION BLOCK'
            while last_character != b'\x17':
                hexx = last_character.hex() # hexadecimal value of byte
                if hexx != '':
                    dec = int(hexx, 16) # decimal representation of hexadecimal byte
                    message += chr(dec)
                else:
                    pass
                try:
                    last_character = connection.read()
                except SerialException:
                    continue
            self.parse(message)