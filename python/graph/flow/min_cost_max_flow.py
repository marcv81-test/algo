from graph import *
from min_cost_path import *

# Finds a minimum-cost maximum flow
# Successive shortest paths algorithm
def ssp(graph, source, sink):
    assert source >= 0 and source < graph.vertices_count
    assert sink >= 0 and sink < graph.vertices_count
    graph.reset_flow()
    total_cost = 0
    total_flow = 0
    while True:
        # Search for a minimum-cost path
        min_cost, previous_edge = bellman_ford(graph, source)
        if min_cost[sink] == infinity:
            return total_cost, total_flow
        # Saturate the minimum-cost path
        path = find_path(previous_edge, source, sink)
        cost, flow = saturate_flow(path)
        total_cost += cost
        total_flow += flow

if __name__ == "__main__":

    ### Tests for correctness ###

    g = Graph(7)
    g.add_edge(0, 1, capacity=5, cost=0)
    g.add_edge(1, 2, capacity=7, cost=1)
    g.add_edge(1, 3, capacity=7, cost=5)
    g.add_edge(2, 3, capacity=2, cost=-2)
    g.add_edge(2, 4, capacity=3, cost=8)
    g.add_edge(3, 4, capacity=3, cost=-3)
    g.add_edge(3, 5, capacity=2, cost=4)
    g.add_edge(4, 6, capacity=3, cost=0)
    g.add_edge(5, 6, capacity=2, cost=0)
    source = 0
    sink = 6

    min_cost, max_flow = ssp(g, source, sink)
    assert min_cost == 12
    assert max_flow == 5

    ### Randomized tests (negative costs, no negative-cost cycle) ###

    import random

    vertices_count = 50
    edges_count = 500
    max_capacity = 1000
    max_cost = 1000

    g = Graph(vertices_count)
    for i in range(edges_count):
        tail = random.randrange(vertices_count - 1)
        head = random.randrange(tail + 1, vertices_count)
        capacity = random.randint(1, max_capacity)
        cost = random.randint(-max_cost, max_cost)
        g.add_edge(tail, head, capacity=capacity, cost=cost)
    source = 0
    sink = vertices_count - 1

    ssp(g, source, sink)
