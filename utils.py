import math

def calc_next_state(current_state, direction):
    curr_x, curr_y = current_state['keeper']
    boxes = current_state['boxes'][:]
    
    if direction == 'w':
        next_positon = curr_x, curr_y-1
        if next_positon in boxes:
            boxes.remove(next_positon)
            boxes.append((curr_x, curr_y-2))
    
    elif direction == 'a':
        next_positon = curr_x-1, curr_y
        if next_positon in boxes:
            boxes.remove(next_positon)
            boxes.append((curr_x-2, curr_y))
                  
    elif direction == 's':
        next_positon = curr_x, curr_y+1
        if next_positon in boxes:
            boxes.remove(next_positon)
            boxes.append((curr_x, curr_y+2))
            
    elif direction == 'd':
        next_positon = curr_x+1, curr_y
        if next_positon in boxes:
            boxes.remove(next_positon)
            boxes.append((curr_x+2, curr_y))
    
    next_state = {'keeper': next_positon, 'boxes': boxes, 'goals': current_state['goals']}  
    return next_state
    
        
def calc_distance(position, list_of_positions, method='manhatan'):
    min_distance = float('inf')
    
    for pos in list_of_positions:
        if method == 'euclidean':
            dist = math.sqrt((pos[0] - position[0]) ** 2 + (pos[1] - position[1]) ** 2)
        elif method == 'manhatan':
            dist = abs(position[0] - pos[0]) + abs(position[1] - pos[1])
        elif method == 'mixed':
            dist1 = math.sqrt((pos[0] - position[0]) ** 2 + (pos[1] - position[1]) ** 2)
            dist2 = abs(position[0] - pos[0]) + abs(position[1] - pos[1])
            dist = min(dist1,dist2)
        if dist < min_distance:
           min_distance = dist     
    return min_distance
