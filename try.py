from z3 import *

# Create a Z3 solver object
solver = Solver()

# Get the current value of the random seed parameter
random_seed = solver.get_param('smt.random_seed')
print("Current random seed:", random_seed)
