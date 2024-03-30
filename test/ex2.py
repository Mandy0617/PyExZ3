from symbolic.args import *

# @concrete(x = 0,y = 0 ) 
# @symbolic(a=1,b=0,c=0) 
import random

# @symbolic(x = -2) 
def ex2(x,y,a):


    if 0<=x+y<= 10: return 0

    elif 10<x-y+a<30: return 1

    elif -10<x*y+a<0: return -1

    else: return -18


    