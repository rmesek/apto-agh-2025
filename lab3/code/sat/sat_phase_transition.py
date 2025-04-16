import random

import matplotlib.pyplot as plt
from timeit import default_timer as timer
import pycosat


def generate_random_clause(n, k):
    """Generate a random clause with k literals from n variables."""
    clause = []
    for _ in range(k):
        variable = random.randint(1, n)  # Choose random variable
        negation = random.choice([1, -1])  # Randomly negate
        clause.append(variable * negation)
    return clause


def generate_random_formula(n, m, k):
    """Generate a random k-CNF formula with n variables and m clauses."""
    formula = []
    for _ in range(m):
        formula.append(generate_random_clause(n, k))
    return formula


def is_satisfiable(formula, n):
    sol = pycosat.solve(formula)
    return sol != "UNSAT"


def plot_results(results, n, k):
    """Plot the phase transition results."""
    a_values = [r[0] for r in results]
    sat_prob = [r[1] for r in results]

    plt.figure(figsize=(10, 6))
    plt.plot(a_values, sat_prob, "o-", linewidth=2)
    plt.grid(True)
    plt.xlabel("α (clauses-to-variables ratio)")
    plt.ylabel("Probability of satisfiability")
    plt.title(f"Phase Transition in {k}-CNF-SAT (n = {n})")
    plt.ylim([-0.05, 1.05])
    plt.savefig(f"phase_transition_k{k}_n{n}.png")
    plt.show()


def run_experiment(n, k, a_values, T):
    """Run the phase transition experiment."""
    results = []

    for a in a_values:
        start_time = timer()
        satisfiable_count = 0
        m = int(a * n)  # Number of clauses

        for _ in range(T):
            formula = generate_random_formula(n, m, k)
            if is_satisfiable(formula, n):
                satisfiable_count += 1

        ratio = satisfiable_count / T
        results.append((a, ratio))
        elapsed = timer() - start_time
        print(f"a = {a:.1f}, S/T = {ratio:.2f}, Time: {elapsed:.2f}s")

    return results
