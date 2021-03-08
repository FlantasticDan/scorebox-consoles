from typing import Dict, Tuple
from .daktronics import Daktronics

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

        self.run()
    
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
        print(potential)