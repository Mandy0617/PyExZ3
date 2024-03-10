# from symbolic.args import *

# @concrete(x = 0,y = 0 ) 
# @symbolic(a=1,b=0,c=0) 
def ex2(a,b,c,x,y):

    if a > 0 :
        while y < a :
            y = y + 1
    else:
        y = 7
        if(b > 0 and b < 9):
            x = 1
        else:
            x = 2
            if c == 0:
                y = y + 3
    
    assert x + y != 8
    