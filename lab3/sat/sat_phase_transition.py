import random
from typing import List

import matplotlib.pyplot as plt
import numpy as np
import pycosat


def get_random_variable(max_var: int) -> int:
    sign = [1, -1]
    variable_number = range(1, max_var + 1)
    var = random.choice(sign) * random.choice(variable_number)
    return var


def get_random_clause(size: int, max_var: int) -> List[int]:
    clause = [get_random_variable(max_var) for _ in range(size)]
    return clause


def get_random_formula(
    clause_no: int, clause_size: int, max_var: int
) -> List[List[int]]:
    formula = [get_random_clause(clause_size, max_var) for _ in range(clause_no)]
    return formula


def is_satisfiable(formula: List[List[int]]) -> bool:
    sol = pycosat.solve(formula)
    return sol != "UNSAT"


def plot_and_show(x: List[float], y: List[float], k, n, repeats) -> None:
    plt.figure(figsize=(10, 6))
    plt.scatter(x, y)
    plt.title(f"(SAT-{k}CNF), n={n}, T={repeats}")
    plt.xlabel("a")
    plt.ylabel("Satisfiability probability")
    plt.savefig("plot.png")
    plt.show()


def calc_sat_probs_and_plot(k, n, repeats) -> None:
    # k = 2  # SAT-kCNF
    # n = 10  # number of variables: x_1, x_2, ..., x_n
    # repeats = 100  # average probability for each one

    max_var = n
    sat_prob = []
    for a in np.arange(1, 10, 0.1):
        clause_no = int(a * n)
        satisfiable_count = 0
        for _ in range(repeats):
            formula = get_random_formula(clause_no, k, max_var)
            satisfiable_count += is_satisfiable(formula)

        probability = satisfiable_count / repeats
        sat_prob.append((a, probability))

    x, y = zip(*sat_prob)
    plot_and_show(x, y, k, n, repeats)
