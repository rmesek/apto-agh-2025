from typing import List, Optional

import pycosat

from sat.types import VertexSets
from utils.dimacs import edgeList


class SortNet:
    def __init__(self, start: int, lines: List[int], generate_equivalences: bool):
        # first available variable
        self.start = start

        # current variable ready to be used
        self.current = start

        # current variables for the input lines
        self.lines = lines.copy()

        # if True, generate equivalences in addition to implications in comparators
        self.generate_equivalences = generate_equivalences

        # current SAT formula
        self.formula = []

    def compare_lines(self, i: int, j: int):
        """
        Compares i-th and j-th lines, higher values go to the earlier line (with
        lower index).
        """
        i = max(i, j)  # will go to the upper wire
        j = min(i, j)  # will go to the lower wire

        # select old and new variables, move ahead
        x_0 = self.lines[i]
        x_1 = self.lines[j]

        y_0 = self.lines[i] = self.current
        y_1 = self.lines[j] = self.current + 1

        self.current += 2

        # add implications to the formula, translated to CNF

        # (x_0 and x_1) => y_0, translates to (~x_0 or ~x_1 or y_0)
        self.formula.append([-x_0, -x_1, y_0])

        # (x_0 or x_1) => y_1, translates to (~x_0 or y_1) and (~x_1 or y_1)
        self.formula.append([-x_0, y_1])
        self.formula.append([-x_1, y_1])

        # add equivalences to the formula
        if self.generate_equivalences:
            # y_0 <=> (x_0 and x_1)
            self.formula.append([-y_0, x_0])
            self.formula.append([-y_0, x_1])

            # y_1 <=> (x_0 or x_1)
            self.formula.append([-y_1, x_0, x_1])


def insertion_sort_formula(a: int, b: int, k: int) -> List[List[int]]:
    """
    Uses sorting network with insertion sort to generate CNF formula for given
    variables.
    """
    lines = list(range(a, b + 1))
    n = len(lines)
    net = SortNet(start=b + 1, lines=lines, generate_equivalences=False)

    # insertion sort on sorting network
    for i in range(1, n):
        for j in range(i, 0, -1):
            net.compare_lines(j, j - 1)

    return net.formula + [[-net.lines[k]]]


def solve_vertex_cover_sortnet(graph: VertexSets, k: int) -> Optional[List[int]]:
    """
    Solve vertex cover problem through reduction to a SAT problem with sorting
    network and using a SAT solver.

    Denote:
    - V = {v_1, v_2, ..., v_n} (n = |V|)
    - k - number of vertices for cover

    Steps for reduction:
    1. For every vertex v_i create variable x_i for i in [1, n]
    2. For every edge (u, v) add clause (u or v) to the formula (ensures that
       every vertex is covered)
    3. Use sorting network to ensure that at most k variables are true

    :param graph: graph as list of sets of neighbors
    :param k: this many vertices have to cover the graph
    :return: solved vertex cover for given k or None if it's not possible
    """
    # add all edges [u, v] to the formula as (u or v)
    formula = edgeList(graph).copy()

    # ensure that at most k variables are selected
    V = len(graph)
    at_most_k_vars_clauses = insertion_sort_formula(1, V - 1, k)

    formula += at_most_k_vars_clauses

    result = pycosat.solve(formula)
    if result == "UNSAT":
        return None
    else:
        # solution exists - translate solution to vertex cover (return those
        # vertices that were selected by the solver, i.e. are positive)
        return [x for x in result if x > 0]
