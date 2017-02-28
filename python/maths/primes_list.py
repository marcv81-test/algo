# Sieve of Eratosthenes
def prime_sieve(n):
    primes = []
    is_prime = [True] * (n + 1)
    for i in range(2, n + 1):
        if is_prime[i] == True:
            primes.append(i)
            for j in range(2 * i, n + 1, i):
                is_prime[j] = False
    return primes

# Sieve of Eratosthenes
# Modified to use half the memory
def prime_sieve_2(n):
    primes = [2]
    is_prime = [True] * (n >> 1)
    for i in range(3, n + 1, 2):
        ii = (i >> 1) - 1
        if is_prime[ii]:
            primes.append(i)
            for j in range(3 * i, n + 1, 2 * i):
                jj = (j >> 1) - 1
                is_prime[jj] = False
    return primes

# Prime factorization, primes only trial division
# The primes parameter must contains all the primes up to at least sqrt(n)
# Returns a dict mapping primes to their multiplicity
def prime_factors(n, primes):
    factors = {}
    for p in primes:
        if n == 1:
            break
        if p * p > n:
            factors[n] = 1
            break
        multiplicity = 0
        q, r = divmod(n, p)
        while r == 0:
            multiplicity += 1
            n = q
            q, r = divmod(n, p)
        if multiplicity > 0:
            factors[p] = multiplicity
    return factors

def expand(factors):
    expansion = 1
    for prime, multiplicity in factors.items():
        expansion *= pow(prime, multiplicity)
    return expansion

def count_divisors(factors):
    total = 1
    for multiplicity in factors.values():
        total *= (multiplicity + 1)
    return total

def sum_divisors(factors):
    total = 1
    for prime, multiplicity in factors.items():
        sub_total = 1
        for i in range(1, multiplicity + 1):
            sub_total += pow(prime, i)
        total *= sub_total
    return total

def gcd(*factors_list):
    gcd = {}
    for prime in set().union(*factors_list):
        multiplicity = min(factors.get(prime, 0) for factors in factors_list)
        if multiplicity > 0:
            gcd[prime] = multiplicity
    return gcd

def lcm(*factors_list):
    lcm = {}
    for prime in set().union(*factors_list):
        multiplicity = max(factors.get(prime, 0) for factors in factors_list)
        lcm[prime] = multiplicity
    return lcm

def multiply(*factors_list):
    product = {}
    for prime in set().union(*factors_list):
        multiplicity = sum(factors.get(prime, 0) for factors in factors_list)
        product[prime] = multiplicity
    return product

def divide(num_factors, den_factors):
    quotient = {}
    for prime in set().union(num_factors, den_factors):
        multiplicity = num_factors.get(prime, 0) - den_factors.get(prime, 0)
        if multiplicity < 0:
            return None
        if multiplicity > 0:
            quotient[prime] = multiplicity
    return quotient

# Tests

primes = prime_sieve(int(1e5))
assert primes[0] == 2
assert primes[-1] == 99991

assert prime_sieve(int(1e6)) == prime_sieve_2(int(1e6))

assert prime_factors(1000000007, primes) == {1000000007: 1}
assert prime_factors(8974892187, primes) == {3: 2, 9973: 1, 99991: 1}

# Divisors of 12: 1, 2, 3, 4, 6, 12
assert count_divisors(prime_factors(12, primes)) == 6
assert sum_divisors(prime_factors(12, primes)) == 28

# gcd(252, 105) == 21
assert expand(gcd(prime_factors(252, primes), prime_factors(105, primes))) == 21

# lcm(252, 105) = 1260
assert expand(lcm(prime_factors(252, primes), prime_factors(105, primes))) == 1260

# 84 * 42 = 3528
assert expand(multiply(prime_factors(84, primes), prime_factors(42, primes))) == 3528

# 3528 / 84 = 42
assert expand(divide(prime_factors(3528, primes), prime_factors(84, primes))) == 42

# 12 / 7 is not an integer
assert divide(prime_factors(12, primes), prime_factors(7, primes)) == None

print(prime_sieve(100))