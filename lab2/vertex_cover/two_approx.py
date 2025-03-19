from typing import List, Set, Tuple

type EdgeList = List[Tuple[int, int]]
type VertexSets = List[Set[int]]


def two_approx_cover(graph: VertexSets) -> Set[int]:
    """
    Two-approximation algorithm for vertex cover.
    :param graph: The graph represented as an adjacency list.
    :return: A set of vertices that form a vertex cover.
    """
    cover = set()
    edges = {(u, v) for u, vs in enumerate(graph[1:], start=1) for v in vs if u < v}
    while edges:
        u, v = edges.pop()
        cover.add(u)
        cover.add(v)
        edges = {edge for edge in edges if u not in edge and v not in edge}
    return cover
