from mapa import is_blocked

def calc_next_position(self, current, direction):
    assert direction in "wasd"
    
    curr_x, curr_y = current
    
    if direction == 'w':
        next_positon = curr_x, curr_y-1
    if direction == 'a':
        next_positon = curr_x-1, curr_y
    if direction == 's':
        next_positon = curr_x, curr_y+1
    if direction == 'd':
        next_positon = curr_x+1, curr_y
        
    # verifica se a posição calculada é um deadlock
    # TODO: possivelmente retornar None em vez da posição atual?    
    if is_blocked(next_positon):
        return current
        
    return next_positon
