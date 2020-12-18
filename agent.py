import asyncio
from tree_search import SokobanSolver
from mapa import Map
from consts import Tiles

class SokobanAgent:
    
    def __init__(self, level: Map, game_settings):
        self.max_steps = game_settings['timeout']
        self.boxes = level.boxes
        self.goals = level.filter_tiles([Tiles.GOAL, Tiles.BOX_ON_GOAL])
        self.keeper = level.keeper
        self.initial_state = {'boxes': self.boxes, 'keeper': self.keeper, 'goals':self.goals}
        self.path_finder : SokobanSolver = SokobanSolver(level_map = level, method='mixed')
        
    def search(self):
        '''
            Passes 1 dictionary to the SokobanSolver's search function:
                -> initial_state = {'boxes': self.boxes, 'keeper': self.keeper, 'goals':self.goals}
            Returns the sequence of moves to be made by the keeper.
        '''
        moves = self.path_finder.search(self.initial_state)
        return moves
    
        
        