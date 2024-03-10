
import gym
from symbolic.args import *
import numpy as np
import math
import random



env = gym.make('Pendulum-v1', g=9.81)
env.reset()

th_init,thdot_init = env.state

print(th_init)
print(thdot_init)

u_init = np.array([1])

@symbolic(th = th_init)
@symbolic(thdot = thdot_init)
@concrete(u = u_init)
# @concrete(u = 1.0)



def pendulum(th, thdot,u):

    g = env.g
    m = env.m
    l = env.l
    dt = env.dt

    u = np.clip(u, -env.max_torque, env.max_torque)[0]
    # u = random.randint(-env.max_torque, env.max_torque)
    env.last_u = u  # for rendering

    costs = angle_normalize(th) ** 2 + 0.1 * thdot**2 + 0.001 * (u**2)

    # costs = th ** 2 + 0.1 * thdot**2 + 0.001 * (u**2)
    newthdot = thdot + (3 * g / (2 * l) * np.sin(th) + 3.0 / (m * l**2) * u) * dt
    # newthdot = thdot + (3 * g / (2 * l) * th + 3.0 / (m * l**2) * u) * dt
    newthdot = np.clip(newthdot, -env.max_speed, env.max_speed)
    newth = th + newthdot * dt

    # env.state = np.array([newth, newthdot])

    if -16 <= costs < -8 : return -1
    if -8 < costs <= 0 : return 1


def angle_normalize(x):
    return ((x + np.pi) % (2 * np.pi)) - np.pi