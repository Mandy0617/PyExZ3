# import random
# from symbolic.args import *

WIDTH = 10
HEIGHT = 10

# @symbolic(x=0,y=0,d = random.choice((1, 2, 3, 4)),v = random.randint(0, 10))
# @concrete(d = random.choice((1, 2, 3, 4)), v = random.uniform(0, 1))
def Navigation(x:float,y:float, d:int,v:float):
    # state = [x,y]
    action = [d,v]
    # x = state[0]
    # y = state[1]
    if action[0] == 1:  # UP
        if y < HEIGHT:
            y += action[1]
    if action[0] == 2:  # RIGHT
        if x < WIDTH:
            x += action[1]
    if action[0] == 3:  # LEFT
        if x > 1:
            x -= action[1]
    if action[0] == 4:  # DOWN
        if y > 1:
            y -= action[1]


    if x == 10:
        if y == 10:
            r = 1000
        else:
            r = -1000
    else:
        r = -1

    newState = (x, y)

    return newState, r



# d = random.choice((1, 2, 3, 4))
# v = random.uniform(0, 1)

# Navigation((0,0), (d, v))

