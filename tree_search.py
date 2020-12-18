from mapa import Map
from utils import *
import asyncio
from queue import PriorityQueue

GOAL_COST = 1
FLOOR_COST = 1.5
KEEPER_MOVE_COST = 2

DIRECTIONS = ["w","a","s","d"]

# Nos de uma arvore de pesquisa
class SearchNode:
    def __init__(self,state,parent,cost=None,heuristic=None,action=''): 
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

    def __lt__(self, other):
        return self.cost + self.heuristic < other.cost + other.heuristic
    def __le__(self, other):
        return self.cost + self.heuristic <= other.cost + other.heuristic
    def __str__(self):
        return "no(" + str(self.state) + "," + str(self.parent) + ")"
    def __repr__(self):
        return str(self)

# Arvores de pesquisa
class SokobanSolver:
    # construtor
    def __init__(self,level_map: Map, method='manhatan'): 
        self.level_map = level_map
        self.boxes_position = []
        self.goals_position = []
        self.deadlocks = []
        self.method = method
        self.deadlocks_pos = []
    
    # obtain the path from the initial state to the goal state
    def get_path(self,node):
        if node.parent == None:
            return [node.action]
        path = self.get_path(node.parent)
        path += [node.action]        
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
            boxes = next_state['boxes']    
            valid_directions.append(direction)
            
            # Check wether we are placing a box outside of the map or
            # placing a box on top of another box  
            if Map.is_blocked(self.level_map,keeper) or len(list(set(boxes))) < len (boxes):
                valid_directions.remove(direction)
                continue

            for box in boxes:
                if box in self.deadlocks_pos:
                    valid_directions.remove(direction)
                    continue
                elif self.isDeadlock(box):
                    self.deadlocks_pos.append(box)  
                    self.deadlocks.append(next_state)
                    valid_directions.remove(direction)
        return list(set(valid_directions))
    

    def heuristic(self, current_state,cost=1,method='manhatan'):
        keeper = current_state['keeper']
        boxes = current_state['boxes']
        goals = current_state['goals']
        heuristic = calc_distance(keeper,boxes,method)
        
        for box in boxes:
            heuristic += calc_distance(box,goals,method)
        return heuristic*cost
        
        
    def cost(self, current_state, direction):
        ''' 
        RECEIVES: the current state and a direction (action)
        RETURNS: the cost of achieving the next state 
            
        Calculates the next state given the current state and a direction (action):
            -> Receives a dictionary containing the current state
            -> Calculates the next state (positions of the keeper and boxes)
            -> Returns the cost of achieving the new state
        '''
        prev_boxes = current_state['boxes']
        next_state = calc_next_state(current_state, direction)
        
        boxes = next_state['boxes']
        for box in boxes:
            if box in self.goals_position:
                return GOAL_COST
        
        # if we moved a box into a normal floor tile    
        boxes.sort()
        prev_boxes.sort()
        if str(boxes) != str(prev_boxes):
            return FLOOR_COST
        
        #if its neither a goal nor moved a box return the cost of a keeper move
        return KEEPER_MOVE_COST
    
    def satisfies(self, current_state):
        ''' 
        RECEIVES: current state
        RETURNS: True or False
        
        Verifies if all the boxes are placed on the goals:
            -> Receives a dictionary containing the current state
            -> Sorts the list containing the positions of the boxes
            -> Checks wether the list is equal to the list containing the goals' position
        '''
        current_state['boxes'].sort()
        return current_state['boxes'] == self.goals_position


    async def search(self, state):
        
        self.goals_position = state['goals']
        self.goals_position.sort()
        
        self.open_nodes = PriorityQueue()
        root = SearchNode(state,None,cost=0,heuristic=self.heuristic(current_state=state,method=self.method))
        self.open_nodes.put((0,root))
        
        open_nodes = 0
        
        while self.open_nodes != []:
            await asyncio.sleep(0)
            node = self.open_nodes.get()[1]

            if self.satisfies(node.state):
                print("OPEN NODES ", open_nodes)
                return self.get_path(node)
            
            for action in self.actions(node.state):
                new_state = self.result(node.state,action)
                
                if new_state not in self.deadlocks:
                    if node.in_parent(new_state):
                        continue
                    
                    acc_cost = (node.cost + self.cost(node.state,action))
                    heur = self.heuristic(new_state, self.cost(node.state,action), self.method)
                    
                    new_node = SearchNode(state=new_state,parent=node,cost=acc_cost,
                                heuristic=heur,action=action)
                    open_nodes += 1 
                    self.open_nodes.put((acc_cost+heur, new_node))
        
        return None

    # auxiliary method for calculating deadlocks
    def isDeadlock(self, pos):
        i_x = 0
        i_y = 0
        list_x = [x[0] for x in self.goals_position]
        list_y = [y[1] for y in self.goals_position]

        if self.level_map.is_blocked(pos):
            return True
        
        if self.level_map.is_blocked((pos[0] + 1, pos[1])) or self.level_map.is_blocked((pos[0] - 1, pos[1])):
            i_x += 1
        if self.level_map.is_blocked((pos[0], pos[1] + 1)) or self.level_map.is_blocked((pos[0], pos[1] - 1)):
            i_y += 1
        
        # verifies if is not on a corner and if it is, make sure it's not a goal
        if (i_x > 0 and i_y > 0) and (pos not in self.goals_position):
           return True
        
        if (i_x > 0 and (pos[0] not in list_x) and (self.level_map.is_blocked((pos[0]+1, pos[1]+1))) and ((self.level_map.is_blocked((pos[0]+1, pos[1]+2)))) and ((self.level_map.is_blocked((pos[0]+1, pos[1]-2)))) and (self.level_map.is_blocked((pos[0]+1,pos[1]-1)))):
            return True
        elif (i_x > 0 and (pos[0] not in list_x) and ((self.level_map.is_blocked((pos[0]-1, pos[1]+1))) and (self.level_map.is_blocked((pos[0]-1, pos[1]+2))) and (self.level_map.is_blocked((pos[0]-1, pos[1]-2))) and (self.level_map.is_blocked((pos[0]-1,pos[1]-1))))):
            return True
        elif (i_y > 0 and (pos[1] not in list_y) and (self.level_map.is_blocked((pos[0]+1, pos[1]+1))) and (self.level_map.is_blocked((pos[0]+2, pos[1]+1))) and (self.level_map.is_blocked((pos[0]-2, pos[1]+1))) and (self.level_map.is_blocked((pos[0]-1, pos[1]+1)))):
            return True
        elif (i_y > 0 and (pos[1] not in list_y) and (self.level_map.is_blocked((pos[0]+1, pos[1]-1))) and (self.level_map.is_blocked((pos[0]+2, pos[1]-1))) and (self.level_map.is_blocked((pos[0]-2, pos[1]-1))) and (self.level_map.is_blocked((pos[0]-1, pos[1]-1)))):
            return True
        
        return False