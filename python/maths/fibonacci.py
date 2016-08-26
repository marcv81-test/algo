def mul_mat(m1, m2):
    ((a, b), (c, d)) = m1
    ((e, f), (g, h)) = m2
    return ((a*e + b*g, a*f + b*h), (c*e + d*g, c*f + d*h))

def mul_mat_vec(m, v):
    ((a, b), (c, d)) = m
    (e, f) = v
    return (a*e + b*f, c*e + d*f)

def exp_mat(m, n):
    m0 = ((1, 0), (0, 1))
    while n > 0:
        if n & 1:
            m0 = mul_mat(m0, m)
        m = mul_mat(m, m)
        n >>= 1
    return m0

def fibonacci(n):
    m = exp_mat(((1, 1), (1, 0)), n)
    v = mul_mat_vec(m, (0, 1))
    return v[0]

def mod_mat(m, mod):
    ((a, b), (c, d)) = m
    return ((a % mod, b % mod), (c % mod, d % mod))

def mod_vec(v, mod):
    (a, b) = v
    return (a % mod, b % mod)

def exp_mod_mat(m, n, mod):
    m0 = ((1, 0), (0, 1))
    while n > 0:
        if n & 1:
            m0 = mod_mat(mul_mat(m0, m), mod)
        m = mod_mat(mul_mat(m, m), mod)
        n >>= 1
    return m0

def fibonacci_mod(n, mod):
    m = exp_mod_mat(((1, 1), (1, 0)), n, mod)
    v = mod_vec(mul_mat_vec(m, (0, 1)), mod)
    return v[0]

assert fibonacci(0) == 0
assert fibonacci(1) == 1
assert fibonacci(2) == 1
assert fibonacci(3) == 2
assert fibonacci(4) == 3
assert fibonacci(5) == 5
assert fibonacci(5) == 5
assert fibonacci(131) == 1066340417491710595814572169

modulo = 1000000007

assert fibonacci_mod(0, modulo) == 0
assert fibonacci_mod(1, modulo) == 1
assert fibonacci_mod(2, modulo) == 1
assert fibonacci_mod(3, modulo) == 2
assert fibonacci_mod(4, modulo) == 3
assert fibonacci_mod(5, modulo) == 5
assert fibonacci_mod(5, modulo) == 5
assert fibonacci_mod(299, modulo) == 248775716
