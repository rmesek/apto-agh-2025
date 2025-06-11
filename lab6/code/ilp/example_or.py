from ortools.linear_solver import pywraplp

def main():
    # create the solver
    solver = pywraplp.Solver.CreateSolver("GLOP")
    if not solver:
        return
    
    # variables
    infinity = solver.infinity()
    x = solver.NumVar(-infinity, infinity, "x")
    y = solver.NumVar(-infinity, infinity, "y")
    print("Number of variables =", solver.NumVariables())
    print("  x =", x)
    print("  y =", y)

    # constraints
    solver.Add(y >= x - 1)
    solver.Add(y >= -4 * x + 4)
    solver.Add(y <= -0.5 * x + 3)
    print("Number of constraints =", solver.NumConstraints())

    # objective function
    solver.Minimize(x + y)

    # solve the problem
    print(f"Solving with {solver.SolverVersion()}")
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print("Solution:")
        print("Objective value =", solver.Objective().Value())
        print("  x =", x.solution_value())
        print("  y =", y.solution_value())
    else:
        print("The problem does not have an optimal solution.")
    
    print(f"Problem solved in {solver.wall_time():d} milliseconds")
    print(f"Problem solved in {solver.iterations():d} iterations")
    print(f"Problem solved in {solver.nodes():d} branch-and-bound nodes")


    
if __name__ == "__main__":
    main()