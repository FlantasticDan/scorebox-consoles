from typing import Dict, List, Tuple
from .daktronics import Daktronics
from .cts import ColoradoTimeSystems, CHANNELS
from .util import get_ordinal

class Volleyball (Daktronics):
    '''Volleyball as scored by a Daktronics All Sport 5000.'''
    def __init__(self, port: str) -> None:
        super().__init__(port)

        # Scoreboard Data
        self.data = {
            'home_score': 0,
            'visitor_score': 0,
            'home_sets': 0,
            'visitor_sets': 0,
            'current_set': 0
        }

        self.runner()
    
    def export(self) -> Dict:
        '''Python Dictionary of Processed Score Data'''
        return self.data
    
    def process(self, message: str, message_range: Tuple[int, int]) -> None:
        self.get_home_score(message, message_range)
        self.get_visitor_score(message, message_range)
        self.get_home_sets(message, message_range)
        self.get_visitor_sets(message, message_range)
        self.get_current_set(message, message_range)

    def get_home_score(self, message, message_range) -> None:
        potential = self.get_field(message, message_range, 108, 4)
        if potential != '':
            self.data['home_score'] = int(potential)
    
    def get_visitor_score(self, message, message_range) -> None:
        potential = self.get_field(message, message_range, 112, 4)
        if potential != '':
            self.data['visitor_score'] = int(potential)
    
    def get_home_sets(self, message, message_range) -> None:
        potential = self.get_field(message, message_range, 215, 2)
        if potential != '':
            self.data['home_sets'] = int(potential)
    
    def get_visitor_sets(self, message, message_range) -> None:
        potential = self.get_field(message, message_range, 217, 2)
        if potential != '':
            self.data['visitor_sets'] = int(potential)
    
    def get_current_set(self, message, message_range) -> None:
        potential = self.get_field(message, message_range, 142, 2)
        if potential != '':
            self.data['current_set'] = int(potential)

class WaterPolo (ColoradoTimeSystems):
    '''Water Polo as scored by a Colorado Time System 6'''
    def __init__(self, port: str, channels = CHANNELS) -> None:
        super().__init__(port)
        self.channels = channels

        # Scoreboard Data
        self.data = {
            'home': 0,
            'visitor': 0,
            'clock': '0:00',
            'shot': '',
            'period': 0
        }

        self.runner()
    
    def export(self) -> Dict:
        '''Python Dictionary of Processed Score Data'''
        return self.data
    
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
                    self.data['clock'] = clock
            # if data[0] != 0 and data[6] != 0 and data[2] != 0:
            #     clock = f'{data[2]}{data[3]}{data[4]}{data[5]}'
            #     if len(clock) > 1:
            #         self.clock = clock[:-2] + ':' + clock[-2:]
            #     else:
            #         self.clock = f':0{clock}'
        if channel == self.channels['shot']:
            if data[4] != 0:
                self.data['shot'] = f'{data[4]}{data[5]}'
        if channel == self.channels['period_shot']:
            if data[1] != '' and data[1] > 0:
                self.data['period'] = str(data[1]) + get_ordinal(data[1])
        if channel == self.channels['scores']:
            if data[0] != 0 and data[6] != 0 and data[2] != 0:
                self.data['home'] = f'{data[0]}{data[1]}'
                self.data['visitor'] = f'{data[6]}{data[7]}'

class WaterPoloDaktronics (Daktronics):
    '''Water Polo as scored by a Daktronics All Sport 5000'''
    def __init__(self, port: str) -> None:
        super().__init__(port)

        # Scoreboard Data
        self.data = {
            'home_score': 0,
            'visitor_score': 0,
            'clock': '0:00',
            'shot': '',
            'period': 0
        }

        self.runner()
    
    def export(self) -> Dict:
        '''Python Dictionary of Processed Score Data'''
        return self.data
    
    def process(self, message: str, message_range: Tuple[int, int]) -> None:
        self.get_home_score(message, message_range)
        self.get_visitor_score(message, message_range)
        self.get_clock(message, message_range)
        self.get_shot_clock(message, message_range)
        self.get_period(message, message_range)
    
    def get_home_score(self, message, message_range) -> None:
        potential = self.get_field(message, message_range, 108, 4)
        if potential != '':
            self.data['home_score'] = int(potential)
    
    def get_visitor_score(self, message, message_range) -> None:
        potential = self.get_field(message, message_range, 112, 4)
        if potential != '':
            self.data['visitor_score'] = int(potential)
    
    def get_clock(self, message, message_range) -> None:
        potential = self.get_field(message, message_range, 1, 5)
        if potential != '':
            self.data['clock'] = potential.lstrip()
    
    def get_shot_clock(self, message, message_range) -> None:
        potential = self.get_field(message, message_range, 201, 8)
        if potential != '':
            self.data['shot'] = int(potential)
    
    def get_period(self, message, message_range) -> None:
        potential = self.get_field(message, message_range, 142, 2)
        if potential != '':
            self.data['period'] = int(potential)

class Football (Daktronics):
    '''Football as scored by a Daktronics All Sport 5000'''
    def __init__(self, port: str) -> None:
        super().__init__(port)

        # Scoreboard Data
        self.data = {
            'home_score': 0,
            'visitor_score': 0,
            'home_timeouts': 0,
            'visitor_timeouts': 0,
            'clock': '0:00',
            'play': 0,
            'quarter': 0,
            'down': '',
            'to_go': 0,
            'ball_on': 0,
            'home_possesion': False,
            'visitor_possesion': False,
            'flag': False
        }

        self.runner()
    
    def export(self) -> Dict:
        '''Python Dictionary of Processed Score Data'''
        return self.data
    
    def process(self, message: str, message_range: Tuple[int, int]) -> None:
        self.get_home_score(message, message_range)
        self.get_visitor_score(message, message_range)
        self.get_home_timeouts(message, message_range)
        self.get_visitor_timeouts(message, message_range)
        self.get_home_possesion(message, message_range)
        self.get_visitor_possesion(message, message_range)
        self.get_clock(message, message_range)
        self.get_play_clock(message, message_range)
        self.get_ball_on(message, message_range)
        self.get_to_go(message, message_range)
        self.get_down(message, message_range)
        self.get_quarter(message, message_range)
        self.get_flag(message, message_range)

    def get_home_score(self, message, message_range) -> None:
        potential = self.get_field(message, message_range, 108, 4)
        if potential != '':
            self.data['home_score'] = int(potential)
    
    def get_visitor_score(self, message, message_range) -> None:
        potential = self.get_field(message, message_range, 112, 4)
        if potential != '':
            self.data['visitor_score'] = int(potential)
    
    def get_clock(self, message, message_range) -> None:
        potential = self.get_field(message, message_range, 1, 5)
        if potential != '':
            self.data['clock'] = potential.lstrip().rstrip()
    
    def get_play_clock(self, message, message_range) -> None:
        potential = self.get_field(message, message_range, 201, 8)
        if potential != '':
            self.data['play'] = potential.lstrip().replace("0:", "").rstrip()
    
    def get_quarter(self, message, message_range) -> None:
        potential = self.get_field(message, message_range, 142, 2)
        if potential != '':
            self.data['quarter'] = int(potential)

    def get_home_timeouts(self, message, message_range) -> None:
        potential = self.get_field(message, message_range, 122, 2)
        if potential != '':
            self.data['home_timeouts'] = int(potential)

    def get_visitor_timeouts(self, message, message_range) -> None:
        potential = self.get_field(message, message_range, 130, 2)
        if potential != '':
            self.data['visitor_timeouts'] = int(potential)
    
    def get_home_possesion(self, message, message_range) -> None:
        potential = self.get_field(message, message_range, 210, 1)
        if potential != '':
            self.data['home_possesion'] = potential == '<'
    
    def get_visitor_possesion(self, message, message_range) -> None:
        potential = self.get_field(message, message_range, 215, 1)
        if potential != '':
            self.data['visitor_possesion'] = potential == '>'
    
    def get_down(self, message, message_range) -> None:
        potential = self.get_field(message, message_range, 222, 3)
        if potential != '':
            self.data['down'] = potential
    
    def get_to_go(self, message, message_range) -> None:
        potential = self.get_field(message, message_range, 225, 2)
        if potential != '':
            self.data['to_go'] = int(potential)
    
    def get_ball_on(self, message, message_range) -> None:
        potential = self.get_field(message, message_range, 220, 2)
        if potential != '':
            self.data['ball_on'] = int(potential)
    
    def get_flag(self, message, message_range) -> None:
        potential = self.get_field(message, message_range, 311, 4)
        if potential != '':
            self.data['flag'] = potential == 'FLAG'