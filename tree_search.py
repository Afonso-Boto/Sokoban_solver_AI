
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

# Dominios de pesquisa
# Permitem calcular
# as accoes possiveis em cada estado, etc
class SearchDomain(ABC):

    # construtor
    @abstractmethod
    def __init__(self):
        pass

    # lista de accoes possiveis num estado
    @abstractmethod
    def actions(self, state):
        pass

    # resultado de uma accao num estado, ou seja, o estado seguinte
    @abstractmethod
    def result(self, state, action):
        pass

    # custo de uma accao num estado
    @abstractmethod
    def cost(self, state, action):
        pass

    # custo estimado de chegar de um estado a outro
    @abstractmethod
    def heuristic(self, state, goal):
        pass

    # test if the given "goal" is satisfied in "state"
    @abstractmethod
    def satisfies(self, state, goal):
        pass


# Problemas concretos a resolver
# dentro de um determinado dominio
class SearchProblem:
    def __init__(self, domain, initial, goal):
        self.domain = domain
        self.initial = initial
        self.goal = goal
    def goal_test(self, state):
        return self.domain.satisfies(state,self.goal)

# Nos de uma arvore de pesquisa
class SearchNode:
    def __init__(self,state,parent,depth,cost,heuristic, action): 
        self.state = state
        self.parent = parent
        self.depth = depth
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
    def __init__(self,problem, strategy='breadth'): 
        self.problem = problem
        root = SearchNode(problem.initial,None,0,0,problem.domain.heuristic(problem.initial,problem.goal),None)
        self.open_nodes = [root]
        self.strategy = strategy
        #self.terminals = 1
        #self.non_terminals = 0

    @property
    def length(self):
        return self.solution.depth

    # property transforma a funcao num getter
    @property    
    def avg_ramification(self):
        return (self.terminals + self.non_terminals -1) / self.non_terminals

    @property
    def cost(self):
        return self.solution.cost

    # obter o caminho (sequencia de estados) da raiz ate um no
    def get_path(self,node):
        if node.parent == None:
            return [node.state]
        path = self.get_path(node.parent)
        path += [node.state]
        return path
    
    def get_plan(self, node):
        if node.parent == None:
            return []
        plan = self.get_plan(node.parent)
        plan += [node.action]
        return plan
    
    @property
    def plan(self):
        return self.get_plan(self.solution)

    # procurar a solucao
    def search(self, limit=None):
        #permite inicializar uma nova arvore de cada vez que é chamada a funcao search
        #faz reset basicamente
        self.terminals = 1
        self.non_terminals = 0
        root = SearchNode(self.problem.initial,None,0,0,self.problem.domain.heuristic(self.problem.initial, self.problem.goal),None)
        self.open_nodes = [root]
        
        
        while self.open_nodes != []:
            node = self.open_nodes.pop(0)
            # sempre que se chega a um no é adicionado aos nao terminais
            self.non_terminals += 1
            self.terminals = len(self.open_nodes)

            if self.problem.goal_test(node.state):
                self.solution = node
                return self.get_path(node)

            lnewnodes = []
            for a in self.problem.domain.actions(node.state):
                newstate = self.problem.domain.result(node.state,a)
                                                                #custo acumulado até ao nó atual     
                newnode = SearchNode(newstate,node,node.depth+1,node.cost+self.problem.domain.cost(node.state, a), 
                                     self.problem.domain.heuristic(newstate,self.problem.goal),a) # estimativa da heuritica do novo no ate ao objetivo
                # se o novo nó não estiver na lista de nós já percorridos 
                # adicionar aos novos estados
                # verifica se existe limite de profundidade, caso contrario
                # verifica se o no esta abaixo do limite estabelecido
                if not node.in_parent(newstate) and (limit is None or newnode.depth <= limit):
                    lnewnodes.append(newnode)
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
