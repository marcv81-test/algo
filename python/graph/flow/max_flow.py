from graph import *

import collections

# Finds a shortest path in the residual graph
# BFS algorithm
def edmonds_karp_bfs(graph, source, sink):
    assert source >= 0 and source < graph.vertices_count
    assert sink >= 0 and sink < graph.vertices_count
    level = [infinity] * graph.vertices_count
    level[source] = 0
    previous_edge = [None] * graph.vertices_count
    todo = collections.deque()
    todo.append(source)
    while len(todo) > 0:
        vertex = todo.popleft()
        next_level = level[vertex] + 1
        edges = (edge
            for edge in graph.edges[vertex]
            if edge.capacity > edge.flow)
        for edge in edges:
            next_vertex = edge.head
            if level[next_vertex] == infinity:
                level[next_vertex] = next_level
                previous_edge[next_vertex] = edge
                if next_vertex == sink:
                    return find_path(previous_edge, source, sink)
                todo.append(next_vertex)

# Finds a maximum flow
# Edmonds-Karp algorithm
# Repeatedly saturates a shortest path in the residual graph
def edmonds_karp(graph, source, sink):
    assert source >= 0 and source < graph.vertices_count
    assert sink >= 0 and sink < graph.vertices_count
    graph.reset_flow()
    total_flow = 0
    while True:
        # Search for a shortest path
        path = edmonds_karp_bfs(graph, source, sink)
        if path is None:
            return total_flow
        # Saturate the shortest path
        cost, flow = saturate_flow(path)
        total_flow += flow

# Assigns a level to each vertex on a shortest path from source to sink
# in the residual graph
# BFS algorithm
# Proceeds from sink to source to limit the dead-ends during the DFS
def dinitz_bfs(graph, source, sink):
    assert source >= 0 and source < graph.vertices_count
    assert sink >= 0 and sink < graph.vertices_count
    level = [infinity] * graph.vertices_count
    level[sink] = 0
    todo = collections.deque()
    todo.append(sink)
    while len(todo) > 0:
        vertex = todo.popleft()
        next_level = level[vertex] + 1
        edges = (edge
            for edge in graph.edges[vertex]
            if edge.reverse.capacity > edge.reverse.flow)
        for edge in edges:
            next_vertex = edge.head
            if level[next_vertex] == infinity:
                level[next_vertex] = next_level
                if next_vertex == source:
                    return level
                todo.append(next_vertex)

# Finds a path from source to sink in a level graph
# DFS algorithm
def dinitz_dfs(graph, level, source, sink):
    assert source >= 0 and source < graph.vertices_count
    assert sink >= 0 and sink < graph.vertices_count
    previous_edge = [None] * graph.vertices_count
    todo = []
    todo.append(source)
    while len(todo) > 0:
        vertex = todo.pop()
        edges = (edge
            for edge in graph.edges[vertex]
            if level[edge.tail] == level[edge.head] + 1
            if edge.capacity > edge.flow)
        for edge in edges:
            next_vertex = edge.head
            previous_edge[next_vertex] = edge
            if next_vertex == sink:
                return find_path(previous_edge, source, sink)
            todo.append(next_vertex)

# Finds a maximum flow
# Dinitz algorithm
# Repeatedly saturates a shortest path in the residual graph
# Saturates all the shortest paths in a level graph together (blocking flow)
def dinitz(graph, source, sink):
    assert source >= 0 and source < graph.vertices_count
    assert sink >= 0 and sink < graph.vertices_count
    graph.reset_flow()
    total_flow = 0
    while True:
        # Create the level graph
        level = dinitz_bfs(graph, source, sink)
        if level is None:
            return total_flow
        while True:
            # Search for a shortest path
            path = dinitz_dfs(graph, level, source, sink)
            if path is None:
                break
            # Saturate the shortest path
            cost, flow = saturate_flow(path)
            total_flow += flow


if __name__ == "__main__":

    ### Tests for correctness ###

    g = Graph(6)
    g.add_edge(0, 1, capacity=10)
    g.add_edge(0, 2, capacity=10)
    g.add_edge(1, 2, capacity=2)
    g.add_edge(1, 3, capacity=4)
    g.add_edge(1, 4, capacity=8)
    g.add_edge(2, 4, capacity=9)
    g.add_edge(3, 5, capacity=10)
    g.add_edge(4, 3, capacity=6)
    g.add_edge(4, 5, capacity=10)
    source = 0
    sink = 5

    # Edmonds-Karp
    max_flow = edmonds_karp(g, source, sink)
    assert max_flow == 19

    # Dinitz
    max_flow = dinitz(g, source, sink)
    assert max_flow == 19

    ### Randomized tests ###

    import random

    vertices_count = 500
    edges_count = 5000
    max_capacity = 1000

    g = Graph(vertices_count)
    for i in range(edges_count):
        tail = random.randrange(vertices_count)
        head = random.randrange(vertices_count)
        capacity = random.randint(1, max_capacity)
        g.add_edge(tail, head, capacity=capacity)
    source = 0
    sink = vertices_count - 1

    max_flow_edmonds_karp = edmonds_karp(g, source, sink)
    max_flow_dinitz = dinitz(g, source, sink)

    assert max_flow_edmonds_karp == max_flow_dinitz
