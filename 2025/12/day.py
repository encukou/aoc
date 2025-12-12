import dataclasses
import sys
import os
from pprint import pp
from functools import cached_property

data = sys.stdin.read().splitlines()
print(data)

@dataclasses.dataclass
class Area:
    size_r: int
    size_c: int
    counts: list[int]

    @cached_property
    def total_space(self):
        return self.size_r * self.size_c

@dataclasses.dataclass
class Shape:
    bits: list[list[list[bool]]]
    population: int

SHAPE_SIZE = 3

shapes = []
areas = []
for line in data:
    if not line:
        rotations = []
        for r in range(4):
            assert len(rotations) <= SHAPE_SIZE
            if current_bits not in rotations:
                rotations.append(current_bits)
            current_bits = list(zip(*(reversed(l) for l in current_bits)))
        shapes.append(Shape(rotations, sum(sum(l) for l in current_bits)))
        del current_bits
    elif line.endswith(':'):
        assert int(line[:-1]) == len(shapes)
        current_bits = []
    elif ':' not in line:
        current_bits.append(tuple(int(c == '#') for c in line))
    else:
        wh, counts = line.split(':')
        size_c, size_r = wh.split('x')
        areas.append(Area(int(size_r), int(size_c), [int(s) for s in counts.split()]))
pp(shapes)

can_fit = 0
for area in areas:
    pp(area)
    total_population = sum(ct * sh.population for ct, sh in zip(area.counts, shapes))
    if area.total_space < total_population:
        print(area.total_space, '<', total_population, '!')
        continue
    print(area.total_space, '>=', total_population)

    n_shapes = sum(area.counts)
    grid_size = area.size_r // SHAPE_SIZE * area.size_c // SHAPE_SIZE
    if grid_size >= n_shapes:
        print(grid_size, '>=', n_shapes, '!')
        can_fit += 1
        continue
    print(grid_size, '<', n_shapes)
    print('problem too tough')
    exit()

print('*** part 1:', can_fit)
