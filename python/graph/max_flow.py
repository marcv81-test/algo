# Dinitz maximum flow algorithm

import collections

class Edge:

    @staticmethod
    def create_twins(capacity):
        forward = Edge(capacity)
        backward = Edge(0)
        forward.twin = backward
        backward.twin = forward
        return (forward, backward)

    def __init__(self, capacity):
        assert capacity >= 0
        self.capacity = capacity
        self.flow = 0

    def residual_capacity(self):
        return self.capacity - self.flow

    def increase_flow(self, flow):
        assert flow > 0
        self.flow += flow
        self.twin.flow -= flow

class Graph:

    def __init__(self, vertices_len, infinity=int(1e50)):
        assert vertices_len >= 2
        self.vertices_len = vertices_len
        self.infinity = infinity
        self.edges = tuple([] for i in range(self.vertices_len))

    def add_edge(self, tail, head, capacity):
        assert tail >= 0 and tail < self.vertices_len
        assert head >= 0 and head < self.vertices_len
        (forward, backward) = Edge.create_twins(capacity)
        forward.head = head
        backward.head = tail
        self.edges[tail].append(forward)
        self.edges[head].append(backward)

    def build_level(self, source, sink):
        assert source >= 0 and source < self.vertices_len
        assert sink >= 0 and sink < self.vertices_len
        self.level = [self.infinity] * self.vertices_len
        todo = collections.deque()
        self.level[source] = 0
        todo.append(source)
        while len(todo) > 0:
            vertex = todo.popleft()
            if self.level[vertex] >= self.level[sink]:
                break
            for edge in self.edges[vertex]:
                if self.level[edge.head] != self.infinity:
                    continue
                if edge.residual_capacity() == 0:
                    continue
                self.level[edge.head] = self.level[vertex] + 1
                todo.append(edge.head)

    def augment(self, vertex, sink, flow):
        assert vertex >= 0 and vertex < self.vertices_len
        assert sink >= 0 and sink < self.vertices_len
        assert flow > 0
        if vertex == sink:
            return 0
        else:
            for edge in self.edges[vertex]:
                if flow == 0:
                    break
                if self.level[edge.head] != self.level[vertex] + 1:
                    continue
                residual_capacity = edge.residual_capacity()
                if residual_capacity == 0:
                    continue
                edge_flow = min(flow, residual_capacity)
                edge_flow -= self.augment(edge.head, sink, edge_flow)
                if edge_flow > 0:
                    edge.increase_flow(edge_flow)
                    flow -= edge_flow
            return flow

    def max_flow(self, source, sink):
        assert source >= 0 and source < self.vertices_len
        assert sink >= 0 and sink < self.vertices_len
        max_flow = 0
        while True:
            self.build_level(source, sink)
            if self.level[sink] == self.infinity:
                return max_flow
            flow = self.infinity
            flow -= self.augment(source, sink, flow)
            max_flow += flow

import random

# Test for correctness

g1 = Graph(6)

g1.add_edge(0, 1, 10)
g1.add_edge(0, 2, 10)
g1.add_edge(1, 2, 2)
g1.add_edge(1, 3, 4)
g1.add_edge(1, 4, 8)
g1.add_edge(2, 4, 9)
g1.add_edge(3, 5, 10)
g1.add_edge(4, 3, 6)
g1.add_edge(4, 5, 10)

assert g1.max_flow(0, 5) == 19

# Larger scale test

vertices_len = 5000
edges_len = 20000
max_capacity = 1000

g2 = Graph(vertices_len)

for i in range(edges_len):
    from_vertex = random.randrange(vertices_len)
    to_vertex = random.randrange(vertices_len)
    capacity = random.randrange(1, max_capacity)
    g2.add_edge(from_vertex, to_vertex, capacity)

g2.max_flow(0, vertices_len - 1)
