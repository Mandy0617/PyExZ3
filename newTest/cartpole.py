
import math
from symbolic.args import *
from CartPoleMDPClass import CartPoleMDP

cart = CartPoleMDP()


@symbolic(x=0,x_dot=0,theta=0,theta_dot=0,action=5)

def cartpole(x,x_dot,theta,theta_dot,action):

    force = action
    costheta = theta    #math.cos(theta)
    sintheta = theta #math.sin(theta)

    temp = (force + cart.polemass_length * theta_dot * theta_dot * sintheta) / cart.total_mass

    thetaacc = (cart.gravity * sintheta - costheta * temp) / (cart.length * (4.0/3.0 - (cart.masspole * costheta * costheta / cart.total_mass)))
    xacc = temp - cart.polemass_length * thetaacc * costheta / cart.total_mass

    new_x_dot = x_dot + cart.tau * xacc
    new_theta_dot = theta_dot + cart.tau * thetaacc

    new_x = x + cart.tau * new_x_dot
    new_theta = theta + cart.tau * new_theta_dot

    if new_theta <= 3.14159:
        val = new_theta
    else:
        val = 2 * 3.14159 - new_theta


    if val < 0.2094 and abs(new_x) < 2.4 :
        result = True
    else: 
        result = False

    return 1.0 if result else -10.0

