class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return '(' + str(self.x) + ', ' + str(self.y) + ')'

    # Returns -1 if angle in [0, pi[
    # Returns 1 if angle in [pi, 2pi[
    def semicircle(self):
        if self.y > 0: return -1
        if self.y < 0: return 1
        if self.x > 0: return -1
        if self.x < 0: return 1
        assert False

    def det(self, other):
        return self.x * other.y - self.y * other.x

    def cmp(self, other):
        semicircle = self.semicircle()
        if semicircle != other.semicircle(): return semicircle
        else: return other.det(self)

import random

# Test angle equality for colinear vectors

assert Point(-1, 2).cmp(Point(-3, 6)) == 0

# Sort list of vectors by angle

a = [Point(1, 0), Point(2, 2), Point(0, 3), Point(-4, 4), Point(-5, 0), Point(-6, -6), Point(0, -7), Point(8, -8)]

b = list(a)
random.shuffle(b)
b = sorted(b, cmp=Point.cmp)

for i in range(len(a)):
    assert a[i] == b[i]
