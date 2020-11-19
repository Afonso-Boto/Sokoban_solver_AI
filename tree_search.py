from mapa import Map
from utils import *

GOAL_COST = 0
FLOOR_COST = 1
KEEPER_MOVE_COST = 2
DEADLOCK_COST = 3


DIRECTIONS = ["w","a","s","d"]

# Nos de uma arvore de pesquisa
class SearchNode:
    def __init__(self,state,parent,cost=None,heuristic=None,action=None): 
        self.state = state
        self.parent = parent
        self.cost = cost
        self.heuristic = heuristic
        self.action = action

    def in_parent(self, newstate):
        if self.parent == None:
            return False
        # verifica se o novo estado e o pai do no atual
        if self.parent.state == newstate:
            return True
        # verifica se o novo estado esta no caminho já percorrido (avo, bisavo, etc)
        return self.parent.in_parent(newstate)

    def __str__(self):
        return "no(" + str(self.state) + "," + str(self.parent) + ")"
    def __repr__(self):
        return str(self)

# Arvores de pesquisa
class SokobanSolver:
    # construtor
    def __init__(self,level_map: Map, strategy='breadth'): 
        self.level_map = level_map
        self.boxes_position = []
        self.goals_position = []
        self.deadlocks = []
        self.strategy = strategy
    
    
    # obtain the path from the initial state to the goal state
    # TODO: change the return, it should only return the move and not the whole state
    def get_path(self,node):
        if node.parent == None:
            return [node.state]
        path = self.get_path(node.parent)
        path += [node.state]
        return path
    

    def result(self, current_state, direction):
        '''
            RECEIVES: the current state and a direction (action)
            RETURNS: the next state 
            
            Calculates the next state given the current state and a direction (action):
                -> Receives a dictionary containing the current state
                -> Calculates the next state (positions of the keeper and boxes)
                -> Returns the new state calculated
        '''
        next_state = calc_next_state(current_state, direction)
        return next_state
    
    
    def actions(self, current_state):
        '''
            RECEIVES: the current state
            RETURNS: a list containing all the valid actions for the state
            
            Calculates all the valid actions for a state:
                -> Receives a dictionary containing the current state
                -> For every direction in "wasd" calculates the next state (positions of the keeper and boxes)
                -> Verifies wether the boxes are in a deadlock
                -> Return a list of valid actions (directions)
        '''
        valid_directions = []
        for direction in DIRECTIONS:
            next_state = calc_next_state(current_state,direction)
            keeper = next_state['keeper']
            boxes = next_state['boxes'][:]
            
            valid_directions.extend(direction)
            if Map.is_blocked(self.level_map,keeper):
                valid_directions.remove(direction)
            
            for box in boxes:
                if Map.is_blocked(self.level_map,box) or self.isDeadlock(box):
                    self.deadlocks.extend(box)
                    valid_directions.remove(direction)
        return list(set(valid_directions))
    
    # TODO: NEEDS REWORK!
    def heuristic(self, current_position, goal_position):
        return -1*len([p for p in goal_position if p in current_position])
    
    
    def cost(self, current_state, direction):
        ''' 
        RECEIVES: the current state and a direction (action)
        RETURNS: the cost of achieving the next state 
            
        Calculates the next state given the current state and a direction (action):
            -> Receives a dictionary containing the current state
            -> Calculates the next state (positions of the keeper and boxes)
            -> Returns the cost of achieving the new state
        '''
        prev_boxes = current_state['boxes'][:]
        next_state = calc_next_state(current_state, direction)
            # check if the next position is a goal
        
        boxes = next_state['boxes'][:]
        boxes.sort()
        prev_boxes.sort()
        for box in boxes:
            if box in self.goals_position:
                return GOAL_COST
                # check if the next position is a deadlock
            elif box in self.deadlocks:
                return DEADLOCK_COST
        
        # if we moved a box into a normal floor tile    
        if str(boxes) != str(prev_boxes):
            return FLOOR_COST
        
        #if its neither a goal, a deadlock nor moved a box return the cost of a keeper move
        return KEEPER_MOVE_COST

    def satisfies(self, current_state):
        ''' 
        RECEIVES: current state
        RETURNS: True or False
        
        Verifies if all the boxes are placed on the goals:
            -> Receives a dictionary containing the current state
            -> Sorts the lists containing the positions of the boxes and goals
            -> Checks wether the lists are equal
        '''
        current_state['boxes'].sort()
        current_state['goals'].sort()
        return current_state['boxes'] == current_state['goals']

    # procurar a solucao
    def search(self, state, goal_state):
        #permite inicializar uma nova arvore de cada vez que é chamada a funcao search
        #faz reset basicamente
        root = SearchNode(state,None,cost=0,heuristic=0)
        self.open_nodes = [root]
        
        while self.open_nodes != []:
            node = self.open_nodes.pop(0)

            if self.satisfies(node.state):
                print("cheguei aqui")
                self.solution = node
                return self.get_path(node)

            lnewnodes = []
            # para cada ação na lista de ações possíveis
            # TODO: ver actions
            for action in self.actions(node.state):
                new_state = self.result(node.state,action)
                print(new_state)
                # TODO: rework these functions
                action_cost = self.cost(node.state, action)
                print(action_cost)
                #accumulated_cost = node.cost + action_cost
                #heuristic_cost = self.heuristic(new_state, goal_state)
                
                #new_node = SearchNode(new_state,node,cost=accumulated_cost,heuristic=heuristic_cost,action=action)
                new_node = SearchNode(new_state,node,0,0,0)
                
                # se o novo nó não estiver na lista de nós já percorridos 
                # adicionar aos novos estados

                if not node.in_parent(new_state):
                    lnewnodes.append(new_node)
            self.add_to_open(lnewnodes)
        return None

    # juntar novos nos a lista de nos abertos de acordo com a estrategia
    def add_to_open(self,lnewnodes):
        if self.strategy == 'breadth':
            self.open_nodes.extend(lnewnodes)
        elif self.strategy == 'uniform':
            self.open_nodes.extend(lnewnodes)
            self.open_nodes.sort(key=lambda node: node.cost)
        elif self.strategy == 'greedy':
            self.open_nodes.extend(lnewnodes)
            self.open_nodes.sort(key=lambda node: node.heuristic)
        elif self.strategy == 'a*':
            self.open_nodes.extend(lnewnodes)
            self.open_nodes.sort(key=lambda node: node.cost + node.heuristic)

    # auxiliary method for calculating deadlocks
    def isDeadlock(self, pos):
        i_x = 0 #number of horizontal wall next to the pos i
        i_y = 0 #number of vertical wall next to the pos i

        if Map.is_blocked(self.level_map,(pos[0] + 1, pos[1])) or Map.is_blocked(self.level_map,(pos[0] - 1, pos[1])):
            i_x += 1
        if Map.is_blocked(self.level_map,(pos[0], pos[1] + 1)) or Map.is_blocked(self.level_map,(pos[0], pos[1] - 1)):
            i_y += 1
        if i_x > 0 and i_y > 0 and str(pos) not in str(Map.empty_goals): # verifies if is not on a corner and if it is, make sure it's not a goal
            return True
        return False