from mapa import is_blocked
from mapa import empty_goals

def calc_next_position(self, current, direction):
    assert direction in "wasd"
    
    curr_x, curr_y = current
    
    if direction == 'w':
        next_positon = curr_x, curr_y+1
    if direction == 'a':
        next_positon = curr_x-1, curr_y
    if direction == 's':
        next_positon = curr_x, curr_y-1
    if direction == 'd':
        next_positon = curr_x+1, curr_y
        
    # verifica se a posição calculada é um deadlock
    # TODO: possivelmente retornar None em vez da posição atual?    
    if is_blocked(next_positon):
        return current
        
    return next_positon

def isDeadlock(self, pos):
    i_x = 0 #number of horizontal wall next to the pos i
    i_y = 0 #number of vertical wall next to the pos i


    if is_blocked((pos[0] + 1, pos[1])) or is_blocked((pos[0] - 1, pos[1])):
        i_x += 1
    
    if is_blocked((pos[0], pos[1] + 1)) or is_blocked((pos[0], pos[1] - 1)):
        i_y += 1
    
    if i_x > 0 and i_y > 0 and pos not in empty_goals: # verifies if is not on a corner and if it is, make sure it's not a goal
        return True
    
    return False
