import sys
from dataclasses import dataclass
from collections import Counter
from functools import cached_property
import pprint

data = sys.stdin.read().splitlines()
print(data)

def get_bit(bits, index):
    return (bits >> index) & 1

def permute_bits(bits, indexes):
    return sum(
        get_bit(bits, index) << i
        for i, index in enumerate(indexes)
    )

def permute_rev(bits, indexes):
    return sum(
        get_bit(bits, i) << index
        for i, index in enumerate(indexes)
    )

@dataclass(frozen=True)
class Pattern:
    size: int
    bits: int

    def __post_init__(self):
        if self.bits >= 2**(self.size**2):
            raise ValueError(self)

    @classmethod
    def parse(cls, spec):
        size = len(spec.strip().split('/'))
        bits = sum(
            (c == '#') << n
            for n, c in enumerate(spec.strip().replace('/', ''), start=0)
        )
        return cls(size, bits)

    def __repr__(self):
        return f'<{self._repr}>({self.bits}@{self.size})'

    @cached_property
    def _repr(self):
        chars = []
        size = self.size
        for i in range(size):
            for j in range(size):
                chars.append('.#'[get_bit(self.bits, i*size+j)])
            chars.append('/')
        return ''.join(chars[:-1])

    def rotate(self):
        if self.size == 2:
            return Pattern(
                2,
                permute_bits(self.bits, (2, 0, 3, 1)),
            )
        elif self.size == 3:
            return Pattern(
                3,
                permute_bits(self.bits, (6, 3, 0,  7, 4, 1,  8, 5, 2)),
            )
        else:
            raise ValueError(self.size)

    def flip(self):
        if self.size == 2:
            return Pattern(
                2,
                permute_bits(self.bits, (1, 0, 3, 2)),
            )
        elif self.size == 3:
            return Pattern(
                3,
                permute_bits(self.bits, (2, 1, 0,  5, 4, 3,  8, 7, 6)),
            )
        else:
            raise ValueError(self.size)

    def step(self, rules):
        if self.size in (2, 3):
            return [rules[self]]
        elif self.size == 4:
            return [Pattern(6, sum(
                permute_rev(pat.bits, dst_indexes)
                for src_indexes, dst_indexes in (
                    ((0, 1,  4, 5), (0, 1, 2,  6, 7, 8,  12, 13, 14)),
                    ((2, 3,  6, 7), (3, 4, 5,  9, 10, 11,  15, 16, 17)),
                    ((8, 9,  12, 13), (18, 19, 20,  24, 25, 26,  30, 31, 32)),
                    ((10, 11,  14, 15), (21, 22, 23,  27, 28, 29,  33, 34, 35)),
                )
                for pat in Pattern(2, permute_bits(self.bits, src_indexes)).step(rules)
            ))]
        elif self.size == 6:
            return (
                Pattern(2, permute_bits(self.bits, (0, 1,  6, 7))).step(rules)
                + Pattern(2, permute_bits(self.bits, (2, 3,  8, 9))).step(rules)
                + Pattern(2, permute_bits(self.bits, (4, 5,  10, 11))).step(rules)
                + Pattern(2, permute_bits(self.bits, (12, 13,  18, 19))).step(rules)
                + Pattern(2, permute_bits(self.bits, (14, 15,  20, 21))).step(rules)
                + Pattern(2, permute_bits(self.bits, (16, 17,  22, 23))).step(rules)
                + Pattern(2, permute_bits(self.bits, (24, 25,  30, 31))).step(rules)
                + Pattern(2, permute_bits(self.bits, (26, 27,  32, 33))).step(rules)
                + Pattern(2, permute_bits(self.bits, (28, 29,  34, 35))).step(rules)
            )
        else:
            raise ValueError(self.size)

rules = {}
for line in data:
    src, dst = line.split('=>')
    sources = set()
    source = orig = Pattern.parse(src)
    print(source)
    for i in range(4):
        sources.add(source)
        sources.add(source.flip())
        print(source, source.flip())
        source = source.rotate()
    assert source == orig, (source, orig)
    #assert not sources.intersection(rules)
    for source in sources:
        rules[source] = Pattern.parse(dst)
pprint.pprint(rules)

def step(grid, rules):
    result = Counter()
    for pattern, n in grid.items():
        for pat in pattern.step(rules):
            result[pat] += n
    return result

def bit_count(grid):
    total = 0
    for pattern, n in grid.items():
        total += pattern.bits.bit_count() * n
    return total

if len(data) < 10:
    NUM_ITERATIONS = 2
else:
    NUM_ITERATIONS = 5

grid = Counter([Pattern.parse('.#./..#/###')])
print(grid)
for i in range(NUM_ITERATIONS):
    grid = step(grid, rules)
    print(f'{i}: {bit_count(grid)} -- {grid}')


print('*** part 1:', bit_count(grid))
# 111 too high



print('*** part 2:', ...)
