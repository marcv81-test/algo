class Edge:

    def __init__(self, tail, head, capacity, cost):
        assert capacity >= 0
        self.tail = tail
        self.head = head
        self.capacity = capacity
        self.cost = cost
        self.flow = 0

    def increase_flow(self, flow):
        assert flow > 0
        self.flow += flow
        self.reverse.flow -= flow

class Graph:

    def __init__(self, vertices_count):
        self.vertices_count = vertices_count
        self.edges = [[] for _ in range(self.vertices_count)]

    def add_edge(self, tail, head, capacity=1, cost=0):
        assert tail >= 0 and tail < self.vertices_count
        assert head >= 0 and head < self.vertices_count
        forward = Edge(tail, head, capacity, cost)
        backward = Edge(head, tail, 0, -cost)
        forward.reverse = backward
        backward.reverse = forward
        self.edges[tail].append(forward)
        self.edges[head].append(backward)
