# Naive range minimum query
rmq_build = lambda table: table
rmq_query = lambda table, i0, i1: min(table[i0:i1+1])

# Undirected graph, possibly an unrooted tree
class Graph:

    def __init__(self, vertices_count):
        assert vertices_count > 0
        self.vertices_count = vertices_count
        self.edges = [[] for _ in range(self.vertices_count)]

    def add_edge(self, u, v):
        assert u >= 0 and u < self.vertices_count
        assert v >= 0 and v < self.vertices_count
        self.edges[u].append(v)
        self.edges[v].append(u)

# Rooted tree
class RootedTree:

    def __init__(self, vertices_count, root=0):
        assert vertices_count > 0
        self.vertices_count = vertices_count
        assert root >= 0 and root < self.vertices_count
        self.root = root
        self.parent = [None] * self.vertices_count
        self.children = [[] for _ in range(self.vertices_count)]

    def add_edge(self, u, v):
        assert u >= 0 and u < self.vertices_count
        assert v >= 0 and v < self.vertices_count
        assert self.parent[v] is None
        self.parent[v] = u
        self.children[u].append(v)

    # Creates a rooted tree from an unrooted tree
    # DFS traversal
    @staticmethod
    def from_graph(graph, root=0):
        tree = RootedTree(graph.vertices_count, root)
        todo = [(None, root)]
        while len(todo) > 0:
            u, v = todo.pop()
            if u is not None:
                tree.add_edge(u, v)
            for w in graph.edges[v]:
                if w != u:
                    todo.append((v, w))
        return tree

# Prepares a rooted tree for lowest common ancestor queries
# DFS traversal, Euler tour technique
def lca_build(tree):
    # Vertices arranged in discovery order
    # and index of the occurence of each vertex in the order
    order = []
    order_index = [None] * tree.vertices_count
    # Euler tour representation of the rooted tree
    # and index of the first occurrence of each vertex in the ETR
    etr = []
    etr_index = [None] * tree.vertices_count
    # DFS: build the ETR and assign the discovery orders
    todo = [(True, tree.root)]
    while len(todo) > 0:
        discover, u = todo.pop()
        if discover:
            assert order_index[u] is None
            order_index[u] = len(order)
            order.append(u)
            for v in tree.children[u]:
                todo.append((False, u))
                todo.append((True, v))
            etr_index[u] = len(etr)
        etr.append(order_index[u])
    # Prepare the ETR for RMQ
    etr_rmq = rmq_build(etr)
    return tree, order, etr_rmq, etr_index

# Queries for the lowest common ancestor between two vertices
def lca_query(lca_tree, u, v):
    tree, order, etr_rmq, etr_index = lca_tree
    assert u >= 0 and u < tree.vertices_count
    assert v >= 0 and v < tree.vertices_count
    i0, i1 = etr_index[u], etr_index[v]
    if i0 > i1: i0, i1 = i1, i0
    return order[rmq_query(etr_rmq, i0, i1)]

### Tests for correctness ###

g = Graph(6)
g.add_edge(0, 1)
g.add_edge(0, 2)
g.add_edge(1, 3)
g.add_edge(1, 4)
g.add_edge(2, 5)

# Root the tree at 0
t = RootedTree.from_graph(g, 0)
lca_t = lca_build(t)

assert lca_query(lca_t, 0, 0) == 0
assert lca_query(lca_t, 0, 5) == 0
assert lca_query(lca_t, 3, 5) == 0
assert lca_query(lca_t, 3, 4) == 1

# Root the tree at 2
t = RootedTree.from_graph(g, 2)
lca_t = lca_build(t)

assert lca_query(lca_t, 3, 4) == 1
assert lca_query(lca_t, 3, 5) == 2
