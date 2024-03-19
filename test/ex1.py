from symbolic.args import *
import random

@symbolic(x = -2) 
def ex1(x):


    if 0<=x<= 10: return 0

    elif 10<x<30: return 1

    elif -10<x<0: return -1

    else: return -18

