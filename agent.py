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
        self.goal_state = {'boxes': self.goals,'goals':self.goals}
        self.prev_state = {}
        self.step_counter = 0
        self.path_finder : SokobanSolver = SokobanSolver(level_map = level)
        
    @property
    def state(self):
        return self.initial_state
    
    @property
    def step(self):
        return self.step_counter
    
    def next_move(self):
        return self.next_move
    
    def update_state(self, new_state):
        # receber posiçao das boxes, e dos goals
        self._state = new_state
        (curr_pos) = self.state['keeper']
        
    async def search(self):
        '''
            Passes 2 dictionaries to the SokobanSolver's search function:
                -> initial_state = {'boxes': self.boxes, 'keeper': self.keeper, 'goals':self.goals}
                -> goal_state = {'boxes': self.goals,'goals':self.goals}
            
            Returns the sequence of moves to be made by the keeper.
        '''
        await asyncio.sleep(0)
        moves = self.path_finder.search(self.initial_state, self.goal_state)
        print(moves)
        return moves
    
        
        