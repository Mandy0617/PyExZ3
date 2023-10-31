from symbolic.args import *

@symbolic(x=0) 
def ex1(x):

    if x == 0: return 0

    if x < 0: 
        return -1
    else: 
        return 1