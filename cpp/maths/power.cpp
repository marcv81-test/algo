#include <cassert>

#define MODULO 1000000007

// x ^ n, exponentiation by squaring
long long pow(long long x, long long n) {
    long long y = 1;
    while (n > 0) {
        if (n & 1) {
            y *= x;
        }
        x *= x;
        n >>= 1;
    }
    return y;
}

// (x ^ n) % m, modular exponentiation by squaring
long long pow_mod(long long x, long long n, long long m) {
    long long y = 1;
    while (n > 0) {
        if (n & 1) {
            y = (x * y) % m;
        }
        x = (x * x) % m;
        n >>= 1;
    }
    return y;
}

// (x ^ -1) % m, modular multiplicative inverse using Euler's theorem
long long mod_inv(long long x, long long m) {
	return pow_mod(x, m - 2, m);
}

int main() {

    assert(pow(123, 0) == 1);
    assert(pow(123, 1) == 123);
    assert(pow(6, 15) == 470184984576);
    assert(pow(7, 12) == 13841287201);

    assert(pow_mod(123, 0, MODULO) == 1);
    assert(pow_mod(123, 1, MODULO) == 123);
    assert(pow_mod(6, 15, MODULO) == 184981286);
    assert(pow_mod(7, 12, MODULO) == 841287110);

    assert(mod_inv(123456789, MODULO) == 18633540);
    assert(mod_inv(123, MODULO) == 886178868);
}
