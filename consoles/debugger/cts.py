from typing import List

from ..cts import ColoradoTimeSystems

class CTSDebugger(ColoradoTimeSystems):
    '''Debug Logger for Colorado Time System 6 consoles'''
    def __init__(self, port: str) -> None:
        super().__init__(port)

        self.data = ''
        self.runner()
    
    def process(self, channel: int, values: List[int], formats: List[int]) -> None:
        print(f'Channel {channel} - {values} - {formats}')

if __name__ == '__main__':
    import sys
    port = sys.argv[-1]
    CTSDebugger(port)