from typing import List, Tuple
import serial
from serial import PARITY_EVEN
from . import SerialConnection

from multiprocessing.connection import Connection

class ColoradoTimeSystems (SerialConnection):
    '''Colorado Time System 1/4" Serial Connection Controller'''
    def __init__(self, port: str) -> None:
        super().__init__(port, 9600, PARITY_EVEN)
    
    def get_channel(self, hexx: hex) -> int:
        initial = int(hexx, 16)
        # Least Significant Bit Indicates the Following Bytes are Values not Formatting
        binary_initial = bin(initial)
        if binary_initial[-1] != '0':
            indicator = 1
        else:
            indicator = -1
        
        # Shift Out the Indicator Bit
        shifted = initial >> 1
        # Mask the 5 Least Significant Bits
        masked = shifted & 31
        # Exclusive OR (XOR) Mask for Address
        return (masked ^ 31) * indicator

    def get_value(self, hexx: hex) -> Tuple[int, int]:
        initial = int(hexx, 16)
        # The zeroth digit is only a single character hex representation
        if initial <= 15:
            digit = 0
        else:
            digit = int(hexx[0])
        raw_value = int(hexx[-1], 16)
        # Exclusive OR (XOR) for Corrected Value
        value = raw_value ^ 15
        return digit, value
    
    def process(self, channel: int, values: List[int], formats: List[int]) -> None:
        '''Re-implement as the sport's channel processor'''
        raise AssertionError('method `process` must be reimplemented for each sport.')

    def update(self, send_pipe: Connection, connection: serial.Serial) -> None:
        values = [''] * 8
        formats = [''] * 8
        channel = 0
        while True:
            bite = connection.read()
            if bite:
                hexx = bite.hex()
                dec = int(hexx, 16)
                # Channels are encoded as > 127 decimals
                if dec > 127:
                    channel_potential = self.get_channel(hexx)
                    if channel_potential < 0 and abs(channel_potential) != abs(channel):
                        self.process(channel, values, formats)
                        send_pipe.send(self.data)
                        # Reset Channel and Digit Values
                        channel = channel_potential
                        values = [''] * 8
                        formats = [''] * 8
                    else:
                        channel = channel_potential
                else:
                    # Bytes not representing a channel are values for the preceeding channel
                    digit, value = self.get_value(hexx)
                    if channel > 0:
                        formats[digit] = value
                    else:
                        values[digit] = value

def get_channel(module: str) -> int:
    '''Gets channel from display module.'''
    return int(module, 16)

CHANNELS = {
    "game_time": get_channel('01'),
    "shot": get_channel('03'),
    "period_shot": get_channel('0e'),
    "scores": get_channel('0d')
}