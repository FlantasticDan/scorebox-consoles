from typing import Dict, List, Tuple
from .daktronics import Daktronics
from .cts import ColoradoTimeSystems, CHANNELS
from .util import get_ordinal

class Volleyball (Daktronics):
    '''Volleyball as scored by a Daktronics All Sport 5000.'''
    def __init__(self, port: str) -> None:
        super().__init__(port)

        self.message = ''
        self.message_range = (0, 0)

        # Scoreboard Data
        self.home_score = 0
        self.visitor_score = 0
        self.home_sets = 0
        self.visitor_sets = 0
        self.current_set = 1

        self.runner()
    
    def export(self) -> Dict:
        '''Python Dictionary of Processed Score Data'''
        return {
            'home_score': self.home_score,
            'visitor_score': self.visitor_score,
            'home_sets': self.home_sets,
            'visitor_set': self.visitor_sets,
            'current_set': self.current_set
        }
    
    def process(self, message: str, message_range: Tuple[int, int]) -> None:
        self.message = message
        self.message_range = message_range

        self.get_home_score()
        self.get_visitor_score()
        self.get_home_sets()
        self.get_visitor_sets()
        self.get_current_set()

    def get_home_score(self) -> None:
        potential = self.get_field(self.message, self.message_range, 108, 4)
        if potential != '':
            self.home_score = int(potential)
    
    def get_visitor_score(self) -> None:
        potential = self.get_field(self.message, self.message_range, 112, 4)
        if potential != '':
            self.visitor_score = int(potential)
    
    def get_home_sets(self) -> None:
        potential = self.get_field(self.message, self.message_range, 215, 2)
        if potential != '':
            self.home_sets = int(potential)
    
    def get_visitor_sets(self) -> None:
        potential = self.get_field(self.message, self.message_range, 217, 2)
        if potential != '':
            self.visitor_sets = int(potential)
    
    def get_current_set(self) -> None:
        potential = self.get_field(self.message, self.message_range, 142, 2)
        if potential != '':
            self.current_set = int(potential)

class WaterPolo (ColoradoTimeSystems):
    '''Water Polo as scored by a Colorado Time System 6'''
    def __init__(self, port: str, channels = CHANNELS) -> None:
        super().__init__(port)
        self.channels = channels

        # Scoreboard Data
        self.home = 0
        self.visitor = 0
        self.clock = '0:00'
        self.shot = '0',
        self.period = '0'

        self.runner()
    
    def export(self) -> Dict:
        '''Python Dictionary of Processed Score Data'''
        return {
            'home': self.home,
            'visitor': self.visitor,
            'clock': self.clock,
            'shot': self.shot,
            'period': self.period
        }
    
    def process(self, channel: int, values: List[int]) -> None:
        data = []
        valid = 0
        # print(channel)
        for value in values:
            if value != 15 and value != '':
                data.append(value)
                valid += 1
            else:
                data.append('')
        # print(data)
        if channel == self.channels['game_time']:
            # print(data)
            if data[0] != 0:
                if data[6] != '' and valid >= 4:
                    clock = f'{data[3]}:{data[4]}{data[5]}'
                else:
                    clock = f':{data[2]}{data[3]}'
                    if valid == 2:
                        clock = f':0{data[3]}'
                if len(clock) > 2:
                    self.clock = clock
            # if data[0] != 0 and data[6] != 0 and data[2] != 0:
            #     clock = f'{data[2]}{data[3]}{data[4]}{data[5]}'
            #     if len(clock) > 1:
            #         self.clock = clock[:-2] + ':' + clock[-2:]
            #     else:
            #         self.clock = f':0{clock}'
        if channel == self.channels['shot']:
            if data[4] != 0:
                self.shot = f'{data[4]}{data[5]}'
        if channel == self.channels['period_shot']:
            if data[1] != '' and data[1] > 0:
                self.period = str(data[1]) + get_ordinal(data[1])
        if channel == self.channels['scores']:
            if data[0] != 0 and data[6] != 0 and data[2] != 0:
                self.home = f'{data[0]}{data[1]}'
                self.visitor = f'{data[6]}{data[7]}'