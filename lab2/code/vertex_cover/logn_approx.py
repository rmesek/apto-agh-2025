from typing import List, Set, Tuple

type EdgeList = List[Tuple[int, int]]
type VertexSets = List[Set[int]]


def is_vertex_cover(graph: VertexSets, cover: Set[int]) -> bool:
    for u, vs in enumerate(graph[1:], start=1):
        # (u, v1), (u, v2), ..., (u, vn) are edges
        if u not in cover:
            # u is not in cover, check neighbors (v1, v2, ..., vn)
            if any(v not in cover for v in vs):
                # if v is not in cover, then (u, v) is not covered
                return False
    return True


def logn_approx_cover(graph: List[Set[int]]) -> Set[int]:
    """
    Logarithmic approximation algorithm for vertex cover.
    :param graph: The graph represented as an adjacency list.
    :return: A set of vertices that form a vertex cover.
    """
    cover = set()
    vertices = {i: set(neighbors) for i, neighbors in enumerate(graph[1:], start=1)}

    while not is_vertex_cover(graph, cover):
        # Select the vertex with the highest degree
        print(f"Cover: {cover}")
        u, neighbors = max(vertices.items(), key=lambda item: len(item[1]))
        cover.add(u)
        # Remove u and its neighbors from the graph
        vertices.pop(u)
    return cover
