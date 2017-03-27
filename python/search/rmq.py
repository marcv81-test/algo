# floor(log2(n))
def log2(n):
    assert n > 0
    return n.bit_length() - 1

assert log2(1) == 0
assert log2(2) == 1
assert log2(255) == 7
assert log2(256) == 8

# Builds the RMQ sparse table in O(n log n) time/space
def rmq_build(a):
    assert len(a) > 0
    table = [a]
    for k in range(log2(len(a))):
        table.append([])
        length = 1 << k
        for i in range(len(table[k]) - length):
            table[k + 1].append(min(
                table[k][i],
                table[k][i + length]))
    return table

# Queries the RMQ sparse table in O(1) time
def rmq_query(table, i0, i1):
    assert i0 >= 0 and i1 >= 0
    assert i0 < len(table[0]) and i1 < len(table[0])
    assert i0 <= i1
    query_length = i1 - i0 + 1
    k = log2(query_length)
    length = 1 << k
    return min(
        table[k][i0],
        table[k][i0 + query_length - length])

# Tests

a = [5, 8, 4, 2, 12, 50, 6, 7, 7, 3]
table = rmq_build(a)
assert rmq_query(table, 0, 0) == min(a[0:1])
assert rmq_query(table, 0, 9) == min(a[0:10])
assert rmq_query(table, 6, 9) == min(a[6:10])

a = ['1']
table = rmq_build(a)
assert rmq_query(table, 0, 0) == min(a[0:1])
