class Agent:
    
    def __init__(self, level: Map, game_settings):
        self.max_steps = game_settings['timeout']

        self.boxes = []
        self.goals = []
        self.state = {}
        self.prev_state = {}
        self.step_counter = 0
        self.path_finder : SokobanSolver = SokobanSolver(level_map = level)
        
    @property
    def state(self):
        return self.state
    
    @property
    def step(self):
        return self.step_counter
    
    def next_move(self):
        return self.next_move
    
    def update_state(self, new_state):
        
        self.state = new_state
        self.step_counter = self.state["step"]
        
        (curr_pos) = self.state['keeper']
        
        