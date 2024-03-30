from z3 import *

# Create a symbolic integer variable
x = Int('x')

# Define the assertion
assertion = Not(Not(0 != If(10 < x, 1, 0)))

# Create a Z3 solver
solver = Solver()

# Add the assertion to the solver
solver.add(assertion)

# Check satisfiability
if solver.check() == sat:
    # If satisfiable, get the model
    model = solver.model()
    # Print the value of x that satisfies the assertion
    print("Satisfiable! x =", model[x])
else:
    print("Not satisfiable!")
