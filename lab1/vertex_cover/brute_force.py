from itertools import combinations
from typing import List, Optional, Set, Tuple

EdgeList = List[Tuple[int, int]]
VertexSets = List[Set[int]]


def brute_force(graph: VertexSets, k: int) -> Optional[Set[int]]:
    verticies = set(range(1, len(graph)))
    for i in range(1, k + 1):
        # check all combinations up to k verticies
        for combination in combinations(verticies, i):
            combination = set(combination)
            if is_vertex_cover(graph, combination):
                return combination
    return None


def is_vertex_cover(graph: VertexSets, cover: Set[int]) -> bool:
    for u, vs in enumerate(graph[1:], start=1):
        # (u, v1), (u, v2), ..., (u, vn) are edges
        if u not in cover:
            # u is not in cover, check neighbors (v1, v2, ..., vn)
            if any(v not in cover for v in vs):
                # if v is not in cover, then (u, v) is not covered
                return False
    return True
