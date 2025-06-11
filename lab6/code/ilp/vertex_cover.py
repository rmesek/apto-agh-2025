from typing import Optional, Set, Tuple

from pulp import *

from ilp.types import VertexSets


def vertex_cover_solver(graph: VertexSets) -> Optional[Tuple[Set[int], int]]:
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
    model = LpProblem("vertex_cover", LpMinimize)

    # objective
    variables = {
        v: LpVariable(str(v), cat="Binary")
        for v, neighbors in enumerate(graph)
        if neighbors
    }  # ignore degree 0 vertices

    model += sum(variables.values())

    # constraints
    for v, neighbors in enumerate(graph):
        for u in neighbors:
            if v < u:
                model += variables[u] + variables[v] >= 1

    model.solve()
    if LpStatus[model.status] == "Optimal":
        result = set()
        for var in model.variables():
            if var.varValue:  # value is 0 or 1
                # we only care about vertices numbers
                result.add(int(var.name))
        return result, len(result)
    else:
        return None
