
from GridWorld import GridWorld_Env
from symbolic.args import *
import random
env = GridWorld_Env(3,3)

# actions = ["left", "up", "right", "down"] # 0=Left, 1=Up, 2=right, 3=Down 

@symbolic (x = 0, y = 0,action = 0 ) # action = 0 or action = random.choice((0,1,2,3))
# @concrete(action = random.choice((0,1,2,3)))
def grid(x,y,action):
    if (x == 0 and action == 0) or (x == env.MAX_HOR_VAL and action == 2):
        return -2
    elif (y == 0 and action == 3) or (y == env.MAX_VER_VAL and action == 1):
        return -2
    elif (x,y) == (env.MAX_HOR_VAL -1, env.MAX_VER_VAL) and action == 2:
        return 0
    elif (x,y) == (env.MAX_HOR_VAL, env.MAX_VER_VAL-1) and action == 1:
        return 0
    else:
        return -1
    
    