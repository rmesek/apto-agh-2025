from sys import argv
from utils.dimacs import loadCNF
from utils.solver import basic_solver


def main():
    cnf_file = argv[1]
    n, cnf = loadCNF(cnf_file)
    # print(f"CNF: {cnf}")
    # print(f"Number of variables: {n}")

    result = basic_solver(cnf)
    print(result)


if __name__ == "__main__":
    main()
