# Ternary search, minimizes cost function
# Cost function must be unimodal on the search interval
def search(cost, start, stop, precision):
    while stop - start > precision:
        p1 = (2 * start + stop) / 3
        p2 = (start + 2 * stop) / 3
        if cost(p1) < cost(p2):
            stop = p2
        else:
            start = p1
    return start

# N-dimensional ternary search, minimizes cost function
# Cost function must be convex on the search interval
def search_dimensions(cost, dimension, starts, stops, precisions):

    result = None

    def partial_search(partial):
        nonlocal cost, dimension, starts, stops, precisions, result
        n = len(partial)
        start = starts[n]
        stop = stops[n]
        precision = precisions[n]
        while stop - start > precision:
            x1 = (2 * start + stop) / 3
            x2 = (start + 2 * stop) / 3
            if n + 1 == dimension:
                cost_x1 = cost(partial + [x1])
                cost_x2 = cost(partial + [x2])
            else:
                cost_x1 = cost(partial_search(partial + [x1]))
                cost_x2 = cost(partial_search(partial + [x2]))
            if cost_x1 < cost_x2:
                stop = x2
            else:
                start = x1
        local_result = partial + [(start + stop) / 2]
        if n + 1 == dimension:
            result = local_result
        return local_result

    partial_search([])
    return result

# Tests

import math

# Ternary seach test

def test(x):
    return pow(x - 1, 2)

result = search(test, -100, 100, 1e-3)
assert math.fabs(result - 1) < 1e-3

# 2D ternary search test

# Rosenbrock's banana function
def banana(point):
    x = 1 - point[0]
    y = point[1] - point[0] * point[0]
    return x * x + 100 * y * y

result = search_dimensions(banana, 2, (-100, -100), (100, 100), (1e-3, 1e-3))
assert math.fabs(result[0] - 1) < 1e-3
assert math.fabs(result[1] - 1) < 1e-3
