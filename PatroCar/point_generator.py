import random
import numpy as np

def Generate_Random_Points(x, y, amount=24, offset=0): #THIS FUNCTION SHOULD BE PRETTIER, WHAT A FUCKING MESS. MAGIC WORKING ANYWAY, DONT TOUCH ANYMORE

    point_list = []
    
    factor = 24

    wall_points = amount // 4
    point_list.append([10+offset, random.randint(0+offset, y/factor+offset)])
    while wall_points > 0:
        if wall_points == 1:
            point_list.append([x/wall_points-10-offset, random.randint(0+offset, y/factor+offset)])
        else:
            point_list.append([x/wall_points-10+offset, random.randint(0+offset, y/factor+offset)])
        wall_points-=1
        
    wall_points = amount // 4
    point_list.append([10+offset, random.randint(y/factor*(factor-1)-offset, y-offset)])
    while wall_points > 0:
        if wall_points == amount // 4:
            point_list.append([x/wall_points-10+offset, random.randint(y/factor*(factor-1)-offset, y-offset)])
        else:
            point_list.append([x/wall_points-10-offset, random.randint(y/factor*(factor-1)-offset, y-offset)])
        wall_points-=1
        
    wall_points = amount // 4
    point_list.append([random.randint(x/factor*(factor-1)-offset, x-offset), 10+offset])
    while wall_points > 0:
        print(wall_points)
        if wall_points >= 2:
            point_list.append([random.randint(x/factor*(factor-1)-offset, x-offset), y/wall_points-10+offset])
        else:
            point_list.append([random.randint(x/factor*(factor-1)-offset, x-offset), y/wall_points-10-offset])
        wall_points-=1
        
    wall_points = amount - ((amount//4)*3)
    point_list.append([random.randint(0+offset, x/factor+offset), 10+offset])
    while wall_points > 0:
        if wall_points <= 1:
            point_list.append([random.randint(0+offset, x/factor+offset), y/wall_points-10-offset])
        else:
            point_list.append([random.randint(0+offset, x/factor+offset), y/wall_points-10+offset])
        wall_points-=1
        
    print(point_list)
    coords = np.array(point_list)
    cc_x, cc_y = coords.mean(0)
    x, y = coords.T
    angles = np.arctan2(x-cc_x, y-cc_y)
    indices = np.argsort(angles)
    return coords[indices]
       