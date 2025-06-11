from typing import Optional, Set, Tuple

from ortools.linear_solver import pywraplp

from ilp.types import VertexSets


def vertex_cover_or_solver(graph: VertexSets) -> Optional[Tuple[Set[int], int]]:
    """
    Solve vertex cover problem through reduction to an ILP problem and using
    an ILP solver.

    Denote:
    - V = {v_1, v_2, ..., v_n} (n = |V|)

    Steps for reduction:
    1. For every vertex v_i create variable x_i for i in [1, n]. It's binary,
       since either x_i is in the vertex cover or it it's not
    2. Objective: minimize x_1 + x_2 + ... + x_n
    3. For every edge (v_i, v_j) at least one vertex has to be in the solution:
       x_i + x_j >= 1

    :param graph: graph as list of sets of neighbors
    :return: solved vertex cover and minimal k found or None, if some problem
    occurred
    """
    # Create the solver
    solver = pywraplp.Solver.CreateSolver('SAT')
    if not solver:
        return None

    # Create binary variables for vertices with at least one neighbor
    variables = {}
    for v, neighbors in enumerate(graph):
        if neighbors:
            variables[v] = solver.IntVar(0, 1, f'x_{v}')

    # Objective: minimize sum of selected vertices
    objective = solver.Objective()
    for var in variables.values():
        objective.SetCoefficient(var, 1)
    objective.SetMinimization()

    # Constraints: for each edge, at least one endpoint must be in the cover
    for v, neighbors in enumerate(graph):
        for u in neighbors:
            if v < u and v in variables and u in variables:
                constraint = solver.Constraint(1, solver.infinity())
                constraint.SetCoefficient(variables[v], 1)
                constraint.SetCoefficient(variables[u], 1)

    # Solve the problem
    status = solver.Solve()
    
    if status == pywraplp.Solver.OPTIMAL:
        print(f"Problem solved in {solver.wall_time():d} milliseconds")
        result = set()
        for v, var in variables.items():
            if var.solution_value() > 0.5:  # Check if variable is set to 1
                result.add(v)
        return result, len(result)
    else:
        return None