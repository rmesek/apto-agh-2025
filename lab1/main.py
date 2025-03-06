from sys import argv

from utils.dimacs import edgeList, isVC, loadGraph
from vertex_cover import brute_force


def main():
    graph_file = argv[1]
    k = int(argv[2])

    G = loadGraph(graph_file)
    # print(f"Graph: {G}")  # vertex 0 is not used
    # print(f"Edges: {edgeList(G)}")

    solution = brute_force(G, k)

    if solution is None:
        print("\033[92mNo solution.\033[0m")
        return
    if isVC(edgeList(G), solution):
        print(f"\033[92mValid solution.\n{solution}\033[0m")
        return
    else:
        print(f"\033[91mInvalid solution.\n{solution}\033[0m")
        return


if __name__ == "__main__":
    main()
