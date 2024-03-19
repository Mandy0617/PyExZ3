# from symbolic.args import *

# @concrete(x = 0,y = 0 ) 
# @symbolic(a=1,b=0,c=0) 
from symbolic.args import *
import random

# @symbolic(x = -2) 
def ex2(x,y,a,b):


    if 0<=x+y<= 10: return 0

    elif 10<x-b<30: return 1

    elif -10<y+a<0: return -1

    else: return -18


    