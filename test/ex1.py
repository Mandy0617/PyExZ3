# from symbolic.args import *
import random

# @symbolic(x) 
def ex1(x:float):


    if x == 0: return 0

    y = random.uniform(0,1)

    if x*y == 1: 
        return -1
    else: 
        return 1