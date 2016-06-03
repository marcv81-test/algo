import heapq

class Graph:

    def __init__(self, vertices_len):
        assert vertices_len > 0
        self.vertices_len = vertices_len
        self.edges = [[] for i in range(vertices_len)]

    def add_edge(self, from_vertex, to_vertex, distance):
        assert from_vertex >= 0 and from_vertex < self.vertices_len
        assert to_vertex >= 0 and to_vertex < self.vertices_len
        assert distance >= 0
        self.edges[from_vertex].append((to_vertex, distance))

    def add_undirected_edge(self, from_vertex, to_vertex, distance):
        self.add_edge(from_vertex, to_vertex, distance)
        self.add_edge(to_vertex, from_vertex, distance)

    def dijkstra(self, from_vertex, infinity=int(1e50)):

        visited = [False] * self.vertices_len
        shortest = [infinity] * self.vertices_len
        todo = []

        shortest[from_vertex] = 0

        heapq.heappush(todo, (0, from_vertex))
        while len(todo) > 0:

            (distance, vertex) = heapq.heappop(todo)
            if visited[vertex]:
                continue
            visited[vertex] = True

            for (next_vertex, extra_distance) in self.edges[vertex]:
                next_distance = distance + extra_distance
                if next_distance < shortest[next_vertex]:
                    shortest[next_vertex] = next_distance
                    heapq.heappush(todo, (next_distance, next_vertex))

        return shortest

import random

# Test for correctness

g1 = Graph(6)
g1.add_undirected_edge(0, 1, 10)
g1.add_undirected_edge(1, 2, 10)
g1.add_undirected_edge(2, 3, 10)
g1.add_undirected_edge(3, 4, 10)
g1.add_undirected_edge(4, 5, 10)
g1.add_undirected_edge(0, 5, 25)
g1.add_undirected_edge(1, 3, 18)

shortest = g1.dijkstra(0)

assert shortest[0] == 0
assert shortest[1] == 10
assert shortest[2] == 20
assert shortest[3] == 28
assert shortest[4] == 35
assert shortest[5] == 25

# Larger scale test

vertices_len = 50000
edges_len = 200000
max_distance = 1000

g2 = Graph(vertices_len)

for i in range(edges_len):
    from_vertex = random.randrange(vertices_len)
    to_vertex = random.randrange(vertices_len)
    distance = random.randrange(1, max_distance)
    g2.add_edge(from_vertex, to_vertex, distance)

g2.dijkstra(0)
