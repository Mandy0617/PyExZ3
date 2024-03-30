from z3 import *
from typing import List

# Define variables
x = Int('x')
y = Int('y')

# Define the Z3 solver
solver = Solver()
solved_models = []

# Add constraints
# solver.add(0 < x + y)
# solver.add(x + y < 10)
solver.set("smt.arith.random_initial_value", True)

solver.add(0 < x )
solver.add(y < 10)

if solved_models: # check if the list is empty
    # solver.add(And([And(x != model[x], y != model[y]) for model in solved_models]))
    solver.add(And([solver.model() != model for model in solved_models]))

i = 0
# Check for satisfiability

while i < 5:
    if solver.check() == sat:
        model = solver.model()
        x_value = model[x].as_long()
        y_value = model[y].as_long()
        print("Solution found:")
        print("x =", x_value)
        print("y =", y_value)

        
        for var in model:
            solver.add(var() != model[var()])

        print(f"current solver: {solver}")



    else:
        print("No solution found.")
    i+=1
