# Hopcroft-Karp maximum cardinality matching algorithm

import collections

class Graph:

    def __init__(self, u_len, v_len, infinity=int(1e50)):
        assert u_len > 0
        assert v_len > 0
        self.u_len = u_len
        self.v_len = v_len
        self.infinity = infinity
        self.nil = self.u_len
        self.edges = [[] for i in range(self.u_len)]

    def add_edge(self, u, v):
        assert u >= 0 and u < self.u_len
        assert v >= 0 and v < self.v_len
        self.edges[u].append(v)

    def build_level(self):
        todo = collections.deque()
        self.level = [self.infinity] * (self.u_len + 1)
        for u in range(self.u_len):
            if self.pair[u] != self.nil:
                continue
            self.level[u] = 0
            todo.append(u)
        while len(todo) > 0:
            u = todo.popleft()
            if self.level[u] >= self.level[self.nil]:
                break
            for v in self.edges[u]:
                next_u = self.back_pair[v]
                if self.level[next_u] != self.infinity:
                    continue
                self.level[next_u] = self.level[u] + 1
                todo.append(next_u)

    def augment(self, u):
        assert u >= 0 and u <= self.u_len
        if u == self.nil:
            return True
        else:
            for v in self.edges[u]:
                next_u = self.back_pair[v]
                if self.level[next_u] != self.level[u] + 1:
                    continue
                if self.augment(next_u):
                    self.pair[u] = v
                    self.back_pair[v] = u
                    return True
            self.level[u] = self.infinity
            return False

    def max_matching(self):
        self.pair = [self.nil] * self.u_len
        self.back_pair = [self.nil] * self.v_len
        max_matching = 0
        while True:
            self.build_level()
            if self.level[self.nil] == self.infinity:
                return max_matching
            for u in range(self.u_len):
                if self.pair[u] != self.nil:
                    continue
                if self.augment(u):
                    max_matching += 1

# Test for correctness

u_len = 3
v_len = 3
bipartite = Graph(u_len, v_len)
bipartite.add_edge(0, 0)
bipartite.add_edge(0, 1)
bipartite.add_edge(1, 0)
bipartite.add_edge(1, 2)
bipartite.add_edge(2, 0)

max_matching = bipartite.max_matching()
assert max_matching == 3
