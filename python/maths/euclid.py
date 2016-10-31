def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def lcm(a, b):
    return a * b // gcd(a, b)

# Returns gcd, s, t such that g = s * a + t * b
def extended_gcd(a, b):
    s, t, ss, tt = 1, 0, 0, 1
    while b != 0:
        q = a // b
        a, b = b, a % b
        s, t, ss, tt = ss, tt, s - q * ss, t - q * tt
    return a, s, t

def mod_inv(a, b):
    bb = b
    s, ss, = 1, 0
    while b != 0:
        q = a // b
        a, b = b, a % b
        s, ss = ss, s - q * ss
    return s % bb

# Basic tests

assert gcd(252, 105) == 21
assert gcd(105, 252) == 21

assert lcm(252, 105) == 1260
assert lcm(105, 252) == 1260

assert extended_gcd(252, 105) == (21, -2, 5)
assert extended_gcd(105, 252) == (21, 5, -2)

assert mod_inv(3, 11) == 4
assert mod_inv(4, 11) == 3

# Fancy n choose k modulo prime demo

modulo = 1000000007
limit = 1000

factorial_mod = [1]
for i in range(1, limit + 1):
    factorial_mod.append(factorial_mod[i - 1] * i % modulo)

factorial_mod_inv = [mod_inv(1, modulo)]
for i in range(1, limit + 1):
    factorial_mod_inv.append(factorial_mod_inv[i - 1] * mod_inv(i, modulo) % modulo)

def nchoosek(n, k):
    assert k >= 0 and k <= limit
    assert n >= k and n <= limit
    return factorial_mod[n] * factorial_mod_inv[k] * factorial_mod_inv[n - k] % modulo

assert nchoosek(10, 5) == 252
assert nchoosek(1000, 500) == 159835829
