infinity = int(1e18)

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

    def reset_flow(self):
        for vertex in range(self.vertices_count):
            for edge in self.edges[vertex]:
                edge.flow = 0

# Finds the list of edges from source to sink
# given the parent-link representation of a tree
def find_path(previous_edge, source, sink):
    vertex = sink
    path = []
    while vertex != source:
        edge = previous_edge[vertex]
        path.append(edge)
        vertex = edge.tail
    return list(reversed(path))

# Saturates the flow on a path
# Returns the increase in cost and flow
def saturate_flow(path):
    cost = 0
    flow = min(edge.capacity - edge.flow for edge in path)
    if flow == 0:
        return 0, 0
    for edge in path:
        cost += edge.cost
        edge.increase_flow(flow)
    cost *= flow
    return cost, flow
