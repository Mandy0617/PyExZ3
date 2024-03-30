from z3 import *
from typing import List

solved_models = []


def solver_1():

    # Define variables
    x = Int('x')
    y = Int('y')

    # Define the Z3 solver
    solver_1 = Solver()
    solver_1.add(0 < x )
    solver_1.add(y < 10)
    if solver_1.check() == sat:
        ass_1 = solver_1.assertions()
        print(f"solver_1 asserts:{ass_1}")

        model_1 = solver_1.model()
    return ass_1, model_1
# Add constraints
# solver.add(0 < x + y)
# solver.add(x + y < 10)

solver_2 = Solver()
ass_1, model_1 = solver_1()

solver_2.add(ass_1)
if solver_2.check() == sat:
    print(f"solver_2 solution: {solver_2.model()}")
else:
    print(f"no solution found")

# if solved_models: # check if the list is empty
#     # solver.add(And([And(x != model[x], y != model[y]) for model in solved_models]))
#     solver_1.add(And([solver_1.model() != model for model in solved_models]))
# if solver_1.check() == sat:
#     ass_1 = solver_1.assertions()
#     print(f"solver_1 asserts:{ass_1}")
    
#     # solver_2.add(ass_1)
#     solver_2 = solver_1
#     ass_2 = solver_2.assertions()
#     print(f"solver_2 asserts:{ass_2}")
#     solver_2.check()
#     ass_3 = solver_2.assertions()
#     print(f"solver_2 asserts after check:{ass_3}")

#     model_1 = solver_1.model()
#     print(f"solver_1 models:{model_1}")

#     model_2 = solver_2.model()
#     print(f"solver_2 models:{model_2}")


# i = 0
# # Check for satisfiability

# while i < 5:
#     if solver_1.check() == sat:
#         model = solver_1.model()
#         x_value = model[x].as_long()
#         y_value = model[y].as_long()
#         print("Solution found:")
#         print("x =", x_value)
#         print("y =", y_value)

        
#         for var in model:
#             solver_1.add(var() != model[var()])

#         print(f"current solver: {solver_1}")



#     else:
#         print("No solution found.")
#     i+=1
