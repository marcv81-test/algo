import math
import operator

def vect_add(v1, v2):
    assert len(v1) == len(v2)
    return tuple(map(operator.add, v1, v2))

def vect_sub(v1, v2):
    assert len(v1) == len(v2)
    return tuple(map(operator.sub, v1, v2))

def vect_scale(v, f):
    return tuple(f * x for x in v)

def vect_norm(v):
    return math.sqrt(sum(x * x for x in v))

# dot(v1, v2) = norm(v1) * norm(v2) * cos(angle)
def vect_dot(v1, v2):
    assert len(v1) == len(v2)
    return sum(v1[i] * v2[i] for i in range(len(v1)))

# norm(cross(v1, v2)) = norm(v1) * norm(v2) * sin(angle)
def vect3d_cross(v1, v2):
    assert len(v1) == 3 and len(v2) == 3
    return (
        v1[1] * v2[2] - v1[2] * v2[1],
        v1[2] * v2[0] - v1[0] * v2[2],
        v1[0] * v2[1] - v1[1] * v2[0])

# det(v1, v2) = norm(v1) * norm(v2) * sin(angle)
def vect2d_det(v1, v2):
    assert len(v1) == 2 and len(v2) == 2
    return v1[0] * v2[1] - v1[1] * v2[0]

# Shortest distance between a point p and a line (p1, p2)
# < 0 if p is at the right of (p1, p2)
# > 0 if p is at the left of (p1, p2)
def vect2d_dist(p, p1, p2):
    line = vect_sub(p2, p1)
    v = vect_sub(p, p1)
    return vect2d_det(line, v) / vect_norm(line) 

# Returns -1 if angle in [0, pi[
# Returns 1 if angle in [pi, 2pi[
def vect2d_semicircle(p):
    if p[1] > 0: return -1
    if p[1] < 0: return 1
    if p[0] > 0: return -1
    if p[0] < 0: return 1
    assert False

# Angle comparison
def vect2d_cmp(p1, p2):
    semicircle = vect2d_semicircle(p1)
    if semicircle != vect2d_semicircle(p2): return semicircle
    else: return vect2d_det(p2, p1)

# Basic tests

assert vect_add((1, 0), (0, 1)) == (1, 1)
assert vect_sub((2, 3), (1, 1)) == (1, 2)
assert vect_scale((1, 0), 2) == (2, 0)
assert vect_norm((3, 4)) == 5

assert vect_dot((1, 0), (0, 1)) == 0

assert vect3d_cross((1, 0, 0), (0, 1, 0)) == (0, 0, 1)
assert vect3d_cross((0, 1, 0), (1, 0, 0)) == (0, 0, -1)

assert vect2d_det((1, 0), (0, 1)) == 1
assert vect2d_det((0, 1), (1, 0)) == -1

# Test distance to line

assert vect2d_dist((1, 0), (0, -1), (0, 1)) == -1
assert vect2d_dist((-1, 0), (0, -1), (0, 1)) == 1

# Test angle equality for collinear vectors

assert vect2d_cmp((-1, 2), (-3, 6)) == 0

# Sort list of vectors by angle

import random
import functools

a = [(1, 0), (2, 2), (0, 3), (-4, 4), (-5, 0), (-6, -6), (0, -7), (8, -8)]
b = list(a)
random.shuffle(b)
b = sorted(b, key=functools.cmp_to_key(vect2d_cmp))
assert a == b
