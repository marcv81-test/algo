#include <cassert>

#define MODULO 1000000007

// GCD using Euclidean algorithm
long long gcd(long long a, long long b) {
    long long r;
    while (b != 0) {
        r = a % b;
        a = b;
        b = r;
    }
    return a;
}

// a ^ (-1) % b, modular multiplicative inverse using extended Euclidean algorithm
long long mod_inv(long long a, long long b) {
    long long bb = b;
    long long s = 1, ss = 0;
    long long q, r, tmp;
    while (b != 0) {
        q = a / b;
        r = a % b;
        a = b;
        b = r;
        tmp = ss;
        ss = s - q * ss;
        s = tmp;
    }
    // sign fix
    tmp = s % bb;
    if (tmp < 0) {
        tmp += bb;
    }
    return tmp;
}

// GCD and Bezout coefficients
struct Bezout {
    long long gcd;
    long long s;
    long long t;
};

// gcd = s * a + t * b, GCD and Bezout coefficients using extended Euclidean algorithm
Bezout bezout(long long a, long long b) {
    long long s = 1, t = 0, ss = 0, tt = 1;
    long long q, r, tmp;
    while (b != 0) {
        q = a / b;
        r = a % b;
        a = b;
        b = r;
        tmp = ss;
        ss = s - q * ss;
        s = tmp;
        tmp = tt;
        tt = t - q * tt;
        t = tmp;
    }
    return {a, s, t};
}

int main() {

    assert(gcd(252, 105) == 21);
    assert(gcd(123000, 96300) == 300);

    assert(mod_inv(123456789, MODULO) == 18633540);
    assert(mod_inv(123, MODULO) == 886178868);

    Bezout b1 = bezout(252, 105);
    assert(b1.gcd == 21);
    assert(b1.gcd == b1.s * 252 + b1.t * 105);

    Bezout b2 = bezout(123000, 96300);
    assert(b2.gcd == 300);
    assert(b2.gcd == b2.s * 123000 + b2.t * 96300);
}
