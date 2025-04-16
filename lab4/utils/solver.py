def simplify_clause(c, v):
    """
    Simplifies a clause based on the assignment (i.e.,
    creates a new copy of the clause, without literals
    set to False; if the clause is satisfied by V,
    returns None):

    :param c: clause, i.e., list of literals
    :param v: assignment of variables
    :return: simplified clause or None
    """
    simplified_clause = []
    for literal in c:
        if literal not in v:
            # Literal is not assigned, keep it
            simplified_clause.append(literal)
        elif v[literal] == 1:
            # Clause is satisfied
            return None
        elif v[literal] == -1:
            # Literal is set to False, skip it
            continue
        else:
            raise ValueError(f"Invalid value for literal {literal}: {v[literal]}")
    return simplified_clause


def simplify_cnf(cnf, v):
    """
    Simplifies a CNF formula based on the assignment (i.e.,
    simplifies each clause).
    If the simplified clause is None, it is skipped.
    If the simplified clause is [], it means that the clause
    is unsatisfied, and None is returned.

    :param cnf: CNF formula, i.e., list of clauses
    :param v: assignment of variables
    :return: simplified CNF formula
    """
    simplified_cnf = []
    for clause in cnf:
        simplified_clause = simplify_clause(clause, v)
        if simplified_clause is None:
            # Clause is satisfied, skip it
            continue
        elif simplified_clause == []:
            # Clause is unsatisfied, return None
            return None
        elif simplified_clause:
            # Clause is not empty, keep it
            simplified_cnf.append(simplified_clause)
    return simplified_cnf


def _basic_solver(cnf, v):
    cnf = simplify_cnf(cnf, v)
    if cnf is None:
        return "UNSAT"
    elif cnf == []:
        return v

    variable = cnf[0][0]

    # Try assigning the variable to True
    v_copy = v.copy()
    v_copy[variable] = 1
    v_copy[-variable] = -1
    result = _basic_solver(cnf, v_copy)
    if result != "UNSAT":
        return result

    # Try assigning the variable to False
    v_copy = v.copy()
    v_copy[variable] = -1
    v_copy[-variable] = 1
    return _basic_solver(cnf, v_copy)


def basic_solver(cnf):
    """
    Basic recursive CNF solver.

    :param cnf: CNF formula, i.e., list of clauses
    :return: assignment of variables or "UNSAT" if the formula is unsatisfiable
    """
    result = _basic_solver(cnf, dict())
    return result
