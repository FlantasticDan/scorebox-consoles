from typing import Tuple

from ..daktronics import Daktronics

class DaktronicsDebugger(Daktronics):
    '''Debug Logger for Daktronics All Sport 5000 consoles'''
    def __init__(self, port: str) -> None:
        super().__init__(port)

        self.data = ''
        self.runner()
    
    def process(self, message: str, message_range: Tuple[int, int]) -> None:
        print(f'Range ({message_range[0]}, {message_range[1]}) - Message {message}')

if __name__ == '__main__':
    import sys
    port = sys.argv[-1]
    DaktronicsDebugger(port)