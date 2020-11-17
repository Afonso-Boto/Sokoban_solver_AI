
# Module: tree_search
# 
# This module provides a set o classes for automated
# problem solving through tree search:
#    SearchDomain  - problem domains
#    SearchProblem - concrete problems to be solved
#    SearchNode    - search tree nodes
#    SearchTree    - search tree with the necessary methods for searhing
#
#  (c) Luis Seabra Lopes
#  Introducao a Inteligencia Artificial, 2012-2019,
#  Inteligência Artificial, 2014-2019

from abc import ABC, abstractmethod
from utils import *

GOAL_COST = 0
FLOOR_COST = 1
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
    
    # updates the the state of the solver   
    def updateSolver(self,boxes_position:list,goals_position:list):
        self.boxes_position = boxes_position
        self.goals_position = goals_position
    
    # obtain the path from the initial state to the goal state
    def get_path(self,node):
        if node.parent == None:
            return [node.state]
        path = self.get_path(node.parent)
        path += [node.state]
        return path
    
    # TODO: fix erro
    def result(self, current_pos, direction):
        state = current_pos['boxes']
        results = []
        for box in state:
            results.append(calc_next_position(box, direction))
        print(results)
        return results
    
    def actions(self, current_pos):
        # every action that doesnt lead us into a deadlock is a valid action
        print(current_pos)
        state = current_pos['boxes']
        valid_directions = []
        for box in state:            
            for direction in DIRECTIONS:
                next_position = calc_next_position(box,direction)
            # if the next position is different from the current one 
            # it means it will not lead to a deadlock
            # we will also add the deadlocks into the a list for future use
                if next_position == current_pos:
                    self.deadlocks.append(next_position)
                else:
                    valid_directions += [direction]
        return list(set(valid_directions))
    
    # TODO: ver isto em condiçoes e procurar uma heuristica melhor
    def heuristic(self, current_position, goal_position):
        return -1*len([p for p in goal_position if p in current_position])
    
    def cost(self, current_pos, direction):
        state = current_pos['boxes']
        valid_directions = []
        for box in state:           
            next_position = calc_next_position(box, direction)
        
        # check if the next position is a goal
        if next_position in self.goals_position:
            return GOAL_COST
        # check if the next position is a deadlock
        elif next_position in self.deadlocks:
            return DEADLOCK_COST
        
        #if its neither a goal nor a deadlock return the cost of a floor tile
        return FLOOR_COST

    def satisfies(self, current_state, goal_state):
        # 'boxes' ser substituido por goal? embora acho que seja a mesma coisa
        return sorted(goal_state['boxes']) == sorted(current_state['boxes'])

    # procurar a solucao
    def search(self, start_position, goal_position):
        #permite inicializar uma nova arvore de cada vez que é chamada a funcao search
        #faz reset basicamente
        root = SearchNode(start_position,None,cost=0,heuristic=0)
        self.open_nodes = [root]
        
        
        while self.open_nodes != []:
            node = self.open_nodes.pop(0)

            if self.satisfies(node.state,goal_position):
                self.solution = node
                return self.get_path(node)

            lnewnodes = []
            # para cada ação na lista de ações possíveis
            for action in self.actions(node.state):
                new_position = self.result(node.state,action)
                
                action_cost = self.cost(node.state, action)
                accumulated_cost = node.cost + action_cost
                heuristic_cost = self.heuristic(new_position, goal_position)
                
                new_node = SearchNode(new_position,node,cost=accumulated_cost,heuristic=heuristic_cost,action=action)
                
                # se o novo nó não estiver na lista de nós já percorridos 
                # adicionar aos novos estados

                if not node.in_parent(new_position):
                    lnewnodes.append(new_node)
            self.add_to_open(lnewnodes)
        return None

    # juntar novos nos a lista de nos abertos de acordo com a estrategia
    def add_to_open(self,lnewnodes):
        if self.strategy == 'breadth':
            self.open_nodes.extend(lnewnodes)
        elif self.strategy == 'depth':
            self.open_nodes[:0] = lnewnodes
        elif self.strategy == 'uniform':
            self.open_nodes.extend(lnewnodes)
            self.open_nodes.sort(key=lambda node: node.cost)
        elif self.strategy == 'greedy':
            self.open_nodes.extend(lnewnodes)
            self.open_nodes.sort(key=lambda node: node.heuristic)
        elif self.strategy == 'a*':
            self.open_nodes.extend(lnewnodes)
            self.open_nodes.sort(key=lambda node: node.cost + node.heuristic)
