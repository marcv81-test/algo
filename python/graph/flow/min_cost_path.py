from graph import *

import heapq

# Finds a minimum-cost path in the residual graph
# Dijkstra's agorithm
def dijkstra(graph, source, sink=-1):
    assert source >= 0 and source < graph.vertices_count
    assert sink >= -1 and sink < graph.vertices_count
    min_cost = [infinity] * graph.vertices_count
    min_cost[source] = 0
    previous_edge = [None] * graph.vertices_count
    visited = [False] * graph.vertices_count
    todo = []
    heapq.heappush(todo, (0, source))
    while len(todo) > 0:
        cost, vertex = heapq.heappop(todo)
        if not visited[vertex]:
            visited[vertex] = True
            if vertex == sink:
                break
            edges = (edge
                for edge in graph.edges[vertex]
                if edge.capacity > edge.flow)
            for edge in edges:
                next_vertex = edge.head
                next_cost = cost + edge.cost
                assert next_cost >= cost
                if next_cost < min_cost[next_vertex]:
                    min_cost[next_vertex] = next_cost
                    previous_edge[next_vertex] = edge
                    heapq.heappush(todo, (next_cost, next_vertex))
    return min_cost, previous_edge

# Finds a minimum-cost path in the residual graph
# Bellman-Ford algorithm
def bellman_ford(graph, source):
    assert source >= 0 and source < graph.vertices_count
    min_cost = [infinity] * graph.vertices_count
    min_cost[source] = 0
    previous_edge = [None] * graph.vertices_count
    todo = set()
    todo.add(source)
    # Loop invariant: before each iteration min_cost[vertex] is
    # the minimum cost from source to vertex following up to k edges
    for k in range(graph.vertices_count):
        new_min_cost = list(min_cost)
        new_todo = set()
        for vertex in todo:
            edges = (edge
                for edge in graph.edges[vertex]
                if edge.capacity > edge.flow)
            for edge in edges:
                next_vertex = edge.head
                next_cost = min_cost[vertex] + edge.cost
                if next_cost < new_min_cost[next_vertex]:
                    new_min_cost[next_vertex] = next_cost
                    previous_edge[next_vertex] = edge
                    new_todo.add(next_vertex)
        min_cost = new_min_cost
        todo = new_todo
        if len(todo) == 0:
            return min_cost, previous_edge
    raise ValueError('negative-cost cycle')


if __name__ == "__main__":

    ### Tests for correctness ###

    g = Graph(4)
    g.add_edge(0, 1, cost=5)
    g.add_edge(1, 2, cost=5)
    g.add_edge(2, 3, cost=5)
    g.add_edge(0, 2, cost=12)
    g.add_edge(1, 3, cost=7)
    source = 0

    # Dijkstra
    min_cost, previous_edge = dijkstra(g, source)
    assert min_cost == [0, 5, 10, 12]

    # Bellman-Ford
    min_cost, previous_edge = bellman_ford(g, source)
    assert min_cost == [0, 5, 10, 12]

    ### Tests for correctness (negative-cost cycles) ###

    # Negative costs, but no negative-cost cycle
    g = Graph(3)
    g.add_edge(0, 1, cost=-1)
    g.add_edge(1, 2, cost=-1)
    source = 0

    min_cost, previous_edge = bellman_ford(g, source)
    assert min_cost == [0, -1, -2]

    # Negative-cost cycle
    g = Graph(3)
    g.add_edge(0, 1, cost=-1)
    g.add_edge(1, 2, cost=-1)
    g.add_edge(2, 0, cost=-1)
    source = 0

    error = False
    try: min_cost, previous_edge = bellman_ford(g, source)
    except ValueError: error = True
    assert error

    ### Randomized tests ###

    import random

    vertices_count = 100
    edges_count = 5000
    max_cost = 1000

    g = Graph(vertices_count)
    for i in range(edges_count):
        tail = random.randrange(vertices_count)
        head = random.randrange(vertices_count)
        cost = random.randint(0, max_cost)
        g.add_edge(tail, head, cost=cost)
    source = random.randrange(vertices_count)
    sink = random.randrange(vertices_count)

    # Dijkstra
    min_cost, previous_edge = dijkstra(g, source, sink)
    dijkstra_cost = min_cost[sink]
    dijkstra_path = find_path(previous_edge, source, sink)

    # Bellman-Ford
    min_cost, previous_edge = bellman_ford(g, source)
    bellman_ford_cost = min_cost[sink]
    bellman_ford_path = find_path(previous_edge, source, sink)

    assert dijkstra_cost == bellman_ford_cost
    assert dijkstra_path == bellman_ford_path
