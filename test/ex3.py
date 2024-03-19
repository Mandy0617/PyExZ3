from symbolic.args import *

@symbolic(x=False) 
def ex3(x):

    if x==True: return 0

    elif x == False: 
        return -1
    else:
        return -2
