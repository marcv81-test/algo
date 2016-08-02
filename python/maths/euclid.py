def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

# Returns gcd, s, t such that g = s * a + t * b
def extended_gcd(a, b):
    s, t, ss, tt = 1, 0, 0, 1
    while b != 0:
        q = a // b
        a, b = b, a % b
        s, t, ss, tt = ss, tt, s - q * ss, t - q * tt
    return a, s, t

def mod_inv(a, b):
    return extended_gcd(a, b)[1] % b

# Basic tests

assert gcd(252, 105) == 21
assert gcd(105, 252) == 21

assert extended_gcd(252, 105) == (21, -2, 5)
assert extended_gcd(105, 252) == (21, 5, -2)

assert mod_inv(3, 11) == 4
assert mod_inv(4, 11) == 3

# Modulo inverse demo

modulo = 1000000007
b = 12345678987654321
a = b * 98765432123456789
assert (a // b) % modulo == ((a % modulo) * mod_inv(b, modulo)) % modulo
