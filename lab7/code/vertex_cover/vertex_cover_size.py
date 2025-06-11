import math
from itertools import combinations
from typing import Iterable

from vertex_cover.types import VertexSets, TreeDecomposition


def check_subgraph_VC(
    graph: VertexSets, vertices_subset: Iterable[int], candidate_vertices: Iterable[int]
):
    """
    Answers the question: if for given graph we check the subgraph given by the
    vertices subset, does the set of candidate vertices create a Vertex Cover
    for this subgraph?

    :param graph: graphs represented as a list of sets (incident vertices)
    :param vertices_subset: vertices of subgraph
    :param candidate_vertices: candidate solution for Vertex Cover
    :returns: whether candidate vertices are a Vertex Cover solution for subgraph
    """
    # check each vertex and its neighbors
    for v in vertices_subset:
        for u in graph[v]:
            # neighbor not in subgraph, omit
            if u not in vertices_subset:
                continue

            # we found 2 neighboring vertices, neither of which is in the candidate
            # solution, so there is an edge not covered, so it is not valid
            if v not in candidate_vertices and u not in candidate_vertices:
                return False

    return True


memoization_table = {}


def f(graph: VertexSets, bags: TreeDecomposition, bag_idx: int, vertex_cover: set[int]):
    # check memoization table, update if we don't have Vertex Cover
    global memoization_table

    vc_str = "-".join([str(v) for v in sorted(vertex_cover)])
    key = f"{bag_idx}|{vc_str}"

    if not check_subgraph_VC(graph, bags[bag_idx].bag, vertex_cover):
        memoization_table[key] = math.inf

    if key in memoization_table:
        return memoization_table[key]

    # if we may have Vertex Cover, and we don't have memoized value, calculate

    # k = |C|
    k = len(vertex_cover)

    # go through each child, for each one select the smallest addition to the
    # parent's Vertex Cover
    for child_idx in bags[bag_idx].children:
        # vertices that are in child, but were not in parent, so they are new
        # and have to be considered
        child_new = bags[child_idx].bag - bags[bag_idx].bag

        # vertices common for child and current Vertex Cover
        common = bags[child_idx].bag & vertex_cover

        # check each subset of child new vertices (that were not in the parent),
        # select the smallest addition to Vertex Cover
        best = math.inf
        for size in range(len(child_new) + 1):
            for child_vc in combinations(child_new, size):
                vc = common | set(child_vc)
                curr = f(graph, bags, child_idx, vc)
                best = min(curr, best)

        k += best - len(common)

    memoization_table[key] = k
    return k


def vertex_cover_size(graph: VertexSets, tree_decomp: TreeDecomposition) -> int:
    """
    Calculates size of minimal Vertex Cover for given graph, using its tree
    decomposition.

    :param graph: graphs represented as a list of sets (incident vertices)
    :param tree_decomp: tree decomposition of graph
    :returns: size of minimal Vertex Cover
    """
    best_k = math.inf

    bag = tree_decomp[1].bag

    for size in range(len(bag) + 1):
        for vertex_cover in combinations(bag, size):
            k = f(graph, tree_decomp, 1, set(vertex_cover))
            if k < best_k:
                best_k = k

    return best_k
