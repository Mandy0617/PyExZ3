from symbolic.args import *
import random

action_space = ['up','down','left','right']
dimension = (54,54)
office_loc = (49,49) #(30,33)
coffee_locs = [(12,18)]
mail_locs = [(22,19)]

def buildforbidden(forbidden_transitions):
 
    # forbidden_transitions = set()
    for x in range(54):
        for y in [0,3,6,9,12,15,18,21,24,27,30,33,36,39,42,45,48,51]:
            forbidden_transitions.add((x,y,action_space[1]))
            forbidden_transitions.add((x,y+2,action_space[0]))
    for y in range(54):
        for x in [0,3,6,9,12,15,18,21,24,27,30,33,36,39,42,45,48,51]:
            forbidden_transitions.add((x,y,action_space[2]))
            forbidden_transitions.add((x+2,y,action_space[3]))
        # adding 'doors'
    for y in [1,4,7,10,13,16,19,22,25,28,31,34,37,40,43,46,49,52]:
        for x in [2,5,8,11,14,17,20,23,26,29,32,35,38,41,44,47,50]:
            forbidden_transitions.remove((x,y,action_space[3]))
            forbidden_transitions.remove((x+1,y,action_space[2]))
    for x in [1,4,7,10,13,16,19,22,25,28,31,34,37,40,43,46,49,52]:
        for y in [2,5,8,11,14,17,20,23,26,29,32,35,38,41,44,47,50]:
            forbidden_transitions.remove((x,y,action_space[0]))
            forbidden_transitions.remove((x,y+1,action_space[1]))


def in_bound (loc):
    flag = False
    if loc[0] < dimension[0] and loc[0] >= 0:
        if loc[1] < dimension[1] and loc[1] >= 0:
            flag = True
    return flag

# @symbolic(a=0,b=0,has_coffee = random.choice((False,True)),has_mail = random.choice((False, True)), action = random.randint(0,3))
@symbolic(a=0,b=0,has_coffee = 0,has_mail = 0, action = 0)


def OfficeWorld (a,b,has_coffee, has_mail, action):
        forbidden_transitions = set()

        buildforbidden(forbidden_transitions)
        current_loc = (2,1)
        reward  = None # the episode's reward (-100 for pitfall, 0 for reaching the goal, and -1 otherwise)
        flag = False # termination flag is true if the agent falls in a pitfall or reaches to the goal
        flag_succ = False
        flag_pitfall = False
        if (a,b,action) not in forbidden_transitions:
            if action == 0: #up
                a -= 1
            elif action == 1: #down
                a += 1
            elif action == 2: #left
                b -= 1
            elif action == 3: #right
                b += 1
        next_loc = tuple([a,b])

        if in_bound(next_loc):
            current_loc = next_loc
        else:
            next_loc = current_loc

        if has_coffee and has_mail and next_loc == office_loc:
            reward = 1000
            flag = True
            flag_succ = True
            state = [next_loc[0],next_loc[1], has_coffee, has_mail]
            # return state, reward, flag, flag_succ, flag_pitfall
            return state, reward, flag, flag_succ
        else:
            reward = 0
            # reward = -1
            flag = False
            flag_succ = False
            if not has_coffee and next_loc in coffee_locs:
                has_coffee = 1
                # reward = 10
            elif not has_mail and next_loc in mail_locs:
                has_mail = 1
                # reward = 10
            state = [next_loc[0],next_loc[1], has_coffee, has_mail]
            # return state, reward, flag, flag_succ, flag_pitfall
            return state, reward, flag, flag_succ
        

