from sys import argv

from utils.dimacs import edgeList, isVC, loadGraph
from vertex_cover import brute_force
from vertex_cover import two_approx_cover
from vertex_cover import logn_approx_cover
from vertex_cover import sim_annealing_cover


def main():
    graph_file = argv[1]
    # k = int(argv[2])

    G = loadGraph(graph_file)
    # print(f"Graph: {G}")  # vertex 0 is not used
    # print(f"Edges: {edgeList(G)}")

    solution = sim_annealing_cover(G)

    if isVC(edgeList(G), solution):
        print(f"\033[92mValid solution.\n{solution}\033[0m")

        brute_force_solution = brute_force(G, len(solution))
        print(f"Brute force solution: \033[92m{brute_force_solution}\033[0m")
        return
    else:
        print(f"\033[91mInvalid solution.\n{solution}\033[0m")

        brute_force_solution = brute_force(G, len(G))
        print(f"Brute force solution: \033[92m{brute_force_solution}\033[0m")
        return


if __name__ == "__main__":
    main()
