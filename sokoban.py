#
#  Module: sokoban
# 
#  Based on the imported "strips" module, the "sokoban" module
#  defines a set of predicates and operators for representing
#  the "Sokoban" planning domain.
#

import time
from strips import *

# Sokoban predicates

class BoxOnFloor(Predicate):
    def __init__(self,box):
        self.args = [box]

class BoxOnGoal(Predicate):
    def __init__(self,box,goal):
        self.args = [box,goal]

'''class PushBox(Predicate):
    def __init__(self,keeper,box):
        self.args = [keeper,box]

class KeeperFree(Predicate):
    def __init__(self):
        self.args = []'''

# Sokoban operators

X='X'
Y='Y'
Z='Z'

# Operations that the Keeper can make

class Up(Operator):
    args = [X,Y]
    # calc pos das boxes e do goal
    # precisa de logica para dedicir os efeitos pos e negs
    # vai ter que ser chamada a partir do agente
    pc   = [BoxOnFloor(X), BoxOnFloor(Y)]
    neg  = []
    pos  = [BoxOnGoal(X,Z),BoxOnFloor(Y)]

class Down(Operator):
    args = [X,Y]
    pc   = [BoxOnFloor(X), BoxOnFloor(Y)]
    neg  = []
    pos  = [BoxOnGoal(X,Z),BoxOnFloor(Y)]

class Right(Operator):
    args = [X]
    pc   = [BoxOnFloor(X), BoxOnFloor(Y)]
    neg  = []
    pos  = [BoxOnGoal(X,Z),BoxOnFloor(Y)]
    
class Left(Operator):
    args = [X]
    pc   = [BoxOnFloor(X), BoxOnFloor(Y)]
    neg  = []
    pos  = [BoxOnGoal(X,Z),BoxOnFloor(Y)]
    

a=(1,4)
b=(3,4)
c=(5,3)
d=(5,4)
e=(1,1)

initial_state = [ BoxOnGoal(a,c), BoxOnFloor(b)] 
#    _
#   / \
#  |  (e)
#  |
#  |                  |c|
# _|___|a|____|b|_____|d|_    
# 

goal_state    = [ BoxOnGoal(a,c), BoxOnGoal(b,d)]

#    _
#   / \
#  |  ( )           |a|
#  |                |e|
#  |                |d|
# _|__________|b|___|c|___    
#




#print('Substitute:',BoxOnGoal(X,Y).substitute({ X : a, Y : b, Z : c}))

#print('Instanciate:',Up.instanciate([a,b]))



sokoban = STRIPS()

print('Actions:',sokoban.actions(initial_state))


# uncomment to test

inittime = time.time()

p = SearchProblem(sokoban,initial_state,goal_state)
t = SearchTree(p, "depth")
t.search(limit=10)

print(t.plan)
print('time=',time.time()-inittime)
print(len(t.open_nodes),' nodes')



