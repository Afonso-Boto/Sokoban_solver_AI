from tree_search import SokobanSolver
from mapa import Map
from consts import Tiles

class SokobanAgent:
    
    def __init__(self, level: Map, game_settings):
        self.max_steps = game_settings['timeout']
        self.boxes = level.boxes
        self.goals = level.filter_tiles([Tiles.GOAL, Tiles.BOX_ON_GOAL])
        self.keeper = level.keeper
        self._state = {'boxes': self.boxes}
        self._goal_state = {'boxes': self.goals}
        self.prev_state = {}
        self.step_counter = 0
        self.path_finder : SokobanSolver = SokobanSolver(level_map = level)
        
    @property
    def state(self):
        return self._state
    
    @property
    def step(self):
        return self.step_counter
    
    def next_move(self):
        return self.next_move
    
    def update_state(self, new_state):
        # receber posiçao das boxes, e dos goals
        self._state = new_state
        (curr_pos) = self.state['keeper']
        
    def search(self):
        moves = self.path_finder.search(self._state, self._goal_state)
        return moves
    
        
        