# Integer square root, Newton's method
def int_sqrt(n):
    x = n
    y = (x + 1) >> 1
    while y < x:
        x = y
        y = (x + (n // x)) >> 1
    return x

assert int_sqrt(100) == 10
assert int_sqrt(10) == 3
