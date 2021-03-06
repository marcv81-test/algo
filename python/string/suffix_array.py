# Builds an encoded integers string from multiple words
# Inserts unique separators between the words
# Assumes lower case Roman alphabet
def build_string(words):
    def generate():
        offset = len(words) - ord('a')
        separator = 0
        for word in words:
            for c in word:
                yield ord(c) + offset
            yield separator
            separator += 1
    return tuple(generate())

# Builds ranks from a sorted list of suffixes
# The rank increases when adjacent suffixes have a different key
def build_ranks(suffixes, keys):
    ranks = [-1] * len(suffixes)
    current_rank = 1
    ranks[suffixes[0]] = current_rank
    for i in range(1, len(suffixes)):
        if keys[suffixes[i-1]] != keys[suffixes[i]]:
            current_rank += 1
        ranks[suffixes[i]] = current_rank
    return tuple(ranks), current_rank

# Builds keys from ranks
# Each key is (rank of suffix, rank of suffix + offset)
def build_keys(ranks, offset):
    def generate():
        offset_ranks = ranks[offset:] + (0,) * offset
        for i in range(len(ranks)):
            yield ranks[i], offset_ranks[i]
    return tuple(generate())

# Manber-Myers O(n log^2 n) algorithm
# Radix sort appears to be overkill in Python
def build_suffix_array(string):
    suffixes = tuple(range(len(string)))
    keys = string
    span = 1
    while True:
        suffixes = tuple(sorted(suffixes, key=lambda x: keys[x]))
        ranks, max_rank = build_ranks(suffixes, keys)
        if max_rank == len(string):
            break
        keys = build_keys(ranks, span)
        span <<= 1
    return suffixes

# Kasai O(n) algorithm
def build_lcp_array(string, suffix_array):
    inverse_suffix_array = [-1] * len(suffix_array)
    for i, suffix in enumerate(suffix_array):
        inverse_suffix_array[suffix] = i
    lcp_array = [-1] * len(suffix_array)
    lcp = 0
    for i in inverse_suffix_array:
        if i > 0:
            i0, i1 = suffix_array[i], suffix_array[i-1]
            while string[i0+lcp] == string[i1+lcp]:
                lcp += 1
            lcp_array[i] = lcp
            lcp = max(0, lcp - 1)
        else:
            lcp = 0
    return tuple(lcp_array)


# Tests

words = ['z', 'ab']
string = build_string(words)
assert string == (27, 0, 2, 3, 1)

suffixes = (2, 0, 1)
keys = (1, 1, 0)
ranks, max_rank = build_ranks(suffixes, keys)
assert ranks == (2, 2, 1)
assert max_rank == 2

ranks = (2, 3, 1)
keys = build_keys(ranks, 1)
assert keys == ((2, 3), (3, 1), (1, 0))

# Naive O(n^2 log n) algorithm for comparison
def build_suffix_array_naive(string):
    return tuple(sorted(range(len(string)), key=lambda x: string[x:]))

# Naive O(n^2) algorithm for comparison
def build_lcp_array_naive(string, suffix_array):
    lcp_array = [-1] * len(suffix_array)
    for i in range(1, len(suffix_array)):
        lcp = 0
        while string[suffix_array[i]+lcp] == string[suffix_array[i-1]+lcp]:
            lcp += 1
        lcp_array[i] = lcp
    return tuple(lcp_array)

words = ['mississippi']
string = build_string(words)
suffix_array = build_suffix_array(string)
assert suffix_array == build_suffix_array_naive(string)
lcp_array = build_lcp_array(string, suffix_array)
assert lcp_array == build_lcp_array_naive(string, suffix_array)

words = ['']
string = build_string(words)
suffix_array = build_suffix_array(string)
assert suffix_array == build_suffix_array_naive(string)
lcp_array = build_lcp_array(string, suffix_array)
assert lcp_array == build_lcp_array_naive(string, suffix_array)

words = ['apple', 'orange', 'banana', 'mango', 'guava']
string = build_string(words)
suffix_array = build_suffix_array(string)
assert suffix_array == build_suffix_array_naive(string)
lcp_array = build_lcp_array(string, suffix_array)
assert lcp_array == build_lcp_array_naive(string, suffix_array)
