import itertools
from pprint import pprint

import numpy

def line_to_boolstring(line):
    return list(line.strip().translate({'.': '\0', '#': '\x01'}))

with open('data.txt') as f:
    rule = numpy.array(
        [c == '#' for c in f.readline().strip()],
        dtype=numpy.int8,
    )
    assert not f.readline().strip()
    image = numpy.array(
        [
            [c == '#' for c in line.strip()]
            for line in f
            if line.strip()
        ],
        dtype=numpy.int8,
    )

print(rule)
print(image)

indices = tuple(enumerate(
    itertools.product(
        [
            slice(0, -2),
            slice(1, -1),
            slice(2, None),
        ],
        repeat=2
    )
))

pprint(indices)

def print_image(header, image):
    print(header)
    for row in numpy.array(['. ', '██'])[image]:
        print(''.join(row))

print_image(f'Start:', image)

outside = 0

for i in range(2):
    padded = numpy.pad(image, 2, constant_values=outside)
    result = numpy.zeros((image.shape[0]+2, image.shape[1]+2), dtype=int)
    for shift, slices in indices:
        result += padded[slices] * (1 << (8-shift))
    result = rule[result]
    image = result
    print_image(f'After iteration {i+1}:', image)
    outside = rule[outside * 0b111111111]
    print('outside:', outside)

print('Part 1:', result.sum())
