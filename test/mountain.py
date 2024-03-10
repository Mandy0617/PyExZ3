import math
from typing import Optional
from mountaincar import Mountain_Car

from symbolic.args import *

import random

import numpy as np

import gym
# from gym.envs.classic_control import mountain_car
from gym import spaces
from gym.envs.classic_control import utils
from gym.error import DependencyNotInstalled

self = Mountain_Car()
state = self.reset()

force = 0.01
gravity = 0.0025
max_speed = 0.07
min_position = -1.2
max_position = 0.6
goal_position = 0.5
goal_velocity = 0

[position,velocity] = state

@symbolic(position=-1)
@symbolic(velocity = 0)
# @concrete(steps=0,max_steps=100)
# @symbolic(action=0)

def mountain(position, velocity):

    action = 2 #random.randint(0,2)
    velocity += (action - 1) * force + math.cos(3 * position) * (-gravity)


    velocity = np.clip(velocity, -max_speed,max_speed)
    position += velocity
    position = np.clip(position, min_position, max_position)
    if position == min_position and velocity < 0:
        velocity = 0

    terminated = bool(
            position >= goal_position and velocity >= goal_velocity
    )
    reward = -1.0
    
    if not terminated: return -1
    else: return 1




# def mountain(position, velocity):


#     new_state,reward,done,success =  self.step(random.randint(0,2))
    
#     if reward == -1: return -1
#     if reward == 1000: return 1000
    

    # if done: return 1
    # else: 
    #     position = new_state[0]
    #     velocity = new_state[1]
    #     return 0
        # return mountain(position,velocity,steps + 1, max_steps)

# def step (self, action_index):
#         # print(self._env.step(action_index))

#         # new_state, reward, done, _ = self._env.step(action_index)
        
#         new_state, reward, done, _, _ = self._env.step(action_index)

#         new_state = np.clip(new_state, a_min=self._env.observation_space.low, a_max=self._env.observation_space.high)
#         self.log_r.append(reward)
#         success = False
#         if done and new_state[0] >= self._env.goal_position: 
#             reward = 1000
#             success = True
#         return self.scale_state(new_state.tolist()), reward, done, success

# def step(self, action: int):
#     # assert self.action_space.contains(
#     #     action
#     # ), f"{action!r} ({type(action)}) invalid"

#     position, velocity = self.state
#     velocity += (action - 1) * self.force + math.cos(3 * position) * (-self.gravity)
#     velocity = np.clip(velocity, -self.max_speed, self.max_speed)
#     position += velocity
#     position = np.clip(position, self.min_position, self.max_position)
#     if position == self.min_position and velocity < 0:
#         velocity = 0

#     terminated = bool(
#         position >= self.goal_position and velocity >= self.goal_velocity
#     )
#     reward = -1.0

#     self.state = (position, velocity)
#     if self.render_mode == "human":
#         self.render()
#     return np.array(self.state, dtype=np.float32), reward, terminated, False, {}