import random

# Finds s, d such that n = 2^s d + 1 and d is odd
def _factorize(n):
    d = n - 1
    s = 0
    while d & 1 == 0:
        s += 1
        d >>= 1
    return s, d

# Tests if a is a compositeness witness
def _witness(n, s, d, a):
    # Fail if a^d % n = 1 or -1
    x = pow(a, d, n)
    if x == 1 or x == n - 1:
        return False
    # Fail if a^(2^r)d % n = -1 for r in [1, s-1]
    for r in range(1, s):
        x = pow(x, 2, n)
        if x == n - 1:
            return False
    # Pass otherwise
    return True

# Miller-Rabin deterministic primality test
def is_prime_d(n):

    assert n >= 1 and n <= pow(2, 64)
    if n == 1:
        return False
    if n == 2:
        return True
    if n & 1 == 0:
        return False

    # Deterministic bases
    # No false-positive up to 2^64
    bases = 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37
    s, d = _factorize(n)
    for a in (a for a in bases if a < n):
        if _witness(n, s, d, a):
            return False
    return True

# Miller-Rabin non-deterministic primality test
def is_prime_nd(n, k=20):

    assert n >= 1
    if n == 1:
        return False
    if n == 2:
        return True
    if n & 1 == 0:
        return False

    # Non-deterministic distinct random bases in [1, n-1]
    # The false-positive probability is at most 1/4^k
    bases = random.sample(range(1, n), min(k, n - 1))
    s, d = _factorize(n)
    for a in bases:
        if _witness(n, s, d, a):
            return False
    return True

# Tests

n = 1000000

# Sieve of Erathosthenes
is_prime = [True] * (n + 1)
is_prime[1] = False
for i in range(2, n + 1):
    if is_prime[i] == True:
        for j in range(2 * i, n + 1, i):
            is_prime[j] = False

for i in range(1, n + 1):
    assert is_prime_d(i) == is_prime[i]

for i in range(1, n + 1):
    assert is_prime_nd(i) == is_prime[i]
