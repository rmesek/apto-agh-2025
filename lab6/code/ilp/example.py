from pulp import *


def solve_and_print_example():
    """
    Example ILP problem solved with PuLP and default CBC solver.
    Problem:
    Minimize x + y (first integers, then real numbers) with constraints:
    y >= x - 1
    y >= -4x + 4
    y <= -0.5x + 3
    """
    model = LpProblem("example_integers", LpMinimize)

    print("INTEGERS")
    x = LpVariable("x", cat="Integer")
    y = LpVariable("y", cat="Integer")

    model += x + y

    model += y >= x - 1
    model += y >= -4 * x + 4
    model += y <= -0.5 * x + 3

    model.solve()
    print("Status:", LpStatus[model.status])
    print("Objective value:", model.objective)
    print("Variable values:")
    for var in model.variables():
        print(var.name, "=", int(var.varValue))
    print("\n")

    model = LpProblem("example_continuous", LpMinimize)

    print("CONTINUOUS")
    # real numbers version
    x = LpVariable("x", cat="Continuous")
    y = LpVariable("y", cat="Continuous")

    model += x + y

    model += y >= x - 1
    model += y >= -4 * x + 4
    model += y <= -0.5 * x + 3

    model.solve()
    print("Status:", LpStatus[model.status])
    print("Objective value:", model.objective)
    print("Variable values:")
    for var in model.variables():
        print(var.name, "=", var.varValue)
    print("\n")
