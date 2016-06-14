class FenwickTree:

    def __init__(self, size):
        self.size = size
        self.array = [0] * self.size

    # Adds delta to values at and after index
    def update(self, index, delta):
        assert index >= 0 and index < self.size
        index += 1
        while index - 1 < self.size:
            self.array[index - 1] += delta
            # Right sibling if any, parent's right sibling otherwise
            index += index & -index

    # Returns value at index
    def query(self, index):
        assert index >= 0 and index < self.size
        index += 1
        value = 0
        while index != 0:
            value += self.array[index - 1]
            # Parent
            index -= index & -index
        return value

class UpdateIndexQueryRange:

    def __init__(self, size):
        self.tree = FenwickTree(size)

    def update_index(self, index, delta):
        self.tree.update(index, delta)

    def query_range(self, index1, index2):
        def query(index):
            if index < 0:
                return 0
            elif index >= self.tree.size:
                index = self.tree.size - 1
            return self.tree.query(index)
        return query(index2) - query(index1 - 1)

class UpdateRangeQueryIndex:

    def __init__(self, size):
        self.tree = FenwickTree(size)

    def update_range(self, index1, index2, delta):
        def update(index, delta):
            if index >= self.tree.size:
                return
            elif index < 0:
                index = 0
            self.tree.update(index, delta)
        update(index1, delta)
        update(index2 + 1, -delta)

    def query_index(self, index):
        return self.tree.query(index)

tree_len = 1000

# Data structure test

t1 = FenwickTree(tree_len)
assert t1.query(0) == 0
assert t1.query(500) == 0
assert t1.query(999) == 0

t1.update(500, 10)
assert t1.query(0) == 0
assert t1.query(499) == 0
assert t1.query(500) == 10
assert t1.query(501) == 10
assert t1.query(999) == 10

t1.update(0, 5)
assert t1.query(0) == 5
assert t1.query(1) == 5
assert t1.query(500) == 15
assert t1.query(999) == 15

t1.update(999, 20)
assert t1.query(0) == 5
assert t1.query(500) == 15
assert t1.query(998) == 15
assert t1.query(999) == 35

# First use case test

t2 = UpdateIndexQueryRange(tree_len)

t2.update_index(0, 1)
t2.update_index(500, 1)
t2.update_index(999, 1)

assert t2.query_range(0, 500) == 2
assert t2.query_range(1, 499) == 0
assert t2.query_range(500, 999) == 2
assert t2.query_range(501, 998) == 0
assert t2.query_range(-999, -1) == 0
assert t2.query_range(-999, 0) == 1
assert t2.query_range(1000, 9999) == 0
assert t2.query_range(999, 9999) == 1
assert t2.query_range(-999, 9999) == 3

# Second use case test

t3 = UpdateRangeQueryIndex(tree_len)

t3.update_range(0, 999, 5)
t3.update_range(-999, 100, 25)
t3.update_range(900, 9999, 50)

assert t3.query_index(0) == 30
assert t3.query_index(100) == 30
assert t3.query_index(101) == 5
assert t3.query_index(899) == 5
assert t3.query_index(900) == 55
assert t3.query_index(999) == 55
