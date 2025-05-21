from typing import List, Optional

import pycosat

from sat.types import VertexSets
from utils.dimacs import edgeList

n = 0


# x: variables 1, 2, 3, ..., n
# y: variables n + 1, n + 2, ...
def y(i, j):
    return int(n + (i + j) * (i + j + 1) / 2 + i) + 1


def cover_edges(formula, graph):
    edges = edgeList(graph)
    new_clauses = [[u, v] for u, v in edges]
    formula.extend(new_clauses)


def set_y_i_0_true(formula):
    new_clauses = [[y(i, 0)] for i in range(n + 1)]
    formula.extend(new_clauses)


def set_y_0_j_false(formula):
    new_clauses = [[-y(0, j)] for j in range(1, n + 1)]
    formula.extend(new_clauses)


def add_implications_for_pairs(formula):
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            formula.extend([[-y(i - 1, j), y(i, j)], [-y(i - 1, j - 1), -i, y(i, j)]])


def solve_vertex_cover_threshold(graph: VertexSets, k: int) -> Optional[List[int]]:
    """
    Solve vertex cover problem through reduction to a SAT problem with threshold
    functions and using a SAT solver.

    Denote:
    - V = {v_1, v_2, ..., v_n} (n = |V|)
    - k - number of vertices for cover

    Steps for reduction:
    1. For every vertex v_i create variable x_i for i in [1, n]
    2. For every edge (u, v) add clause (u or v) to the formula (ensures that
       every vertex is covered)
    3. Create variables y_i_j; i in [0, n], j in [0, n]; y_i_j is true, if
       for variables x_1, x_2, ..., x_i at least j are true (false otherwise)
    4. Set y_i_0 for all i to true (ensures cover), y_0_j for j > 0 to false
       (there can be at most 100% true variables)
    5. For every pair (i, j) (1 <= i, j <= n) add implication:
       (y_i-1_j => y_i_j) and ((y_i-1_j-1 and x_i) => y_i_j)
       This can be transformed to CNF form (using a => b <=> -a or b):
       (-y_i-1_j or y_i_j) and (-y_i-1_j-1 or -x_i or y_i_j)
    6. Add clause -y_n_k+1 (ensure that at most k vertices are used)

    :param graph: graph as list of sets of neighbors
    :param k: this many vertices have to cover the graph
    :return: solved vertex cover for given k or None if it's not possible
    """
    global n
    formula = []

    n = len(graph)

    vertices = [[v, -v] for v in range(1, n)]
    formula.extend(vertices)

    cover_edges(formula, graph)
    set_y_i_0_true(formula)
    set_y_0_j_false(formula)  # for j > 0

    add_implications_for_pairs(formula)
    formula.append([-y(n, k + 1)])

    result = pycosat.solve(formula)
    if result == "UNSAT":
        return None
    else:
        x_values = result[:n]  # check only x_i variables

        # if variable was chosen (> 0), translate it back and add to result
        result = [x_var for x_var in x_values if x_var > 0]
        return result
