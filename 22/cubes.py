import re
import bisect

import numpy

instructions = []

tr = {
    'on': 1,
    'off': 0,
}

minimum = -50
maximum = 51
with open('data.txt') as f:
    for line in f:
        print(line.strip())
        match = re.match(
            r"(\w+) x=(-?\d+)..(-?\d+),y=(-?\d+)..(-?\d+),z=(-?\d+)..(-?\d+)",
            line.strip(),
        )
        instructions.append((
            tr[match[1]],
            (int(match[2]), int(match[3])),
            (int(match[4]), int(match[5])),
            (int(match[6]), int(match[7])),
        ))

state = numpy.zeros(
    (maximum-minimum, maximum-minimum, maximum-minimum),
    dtype=int,
)
print(state.shape)

for onoff, *coords in instructions:
    state[tuple(slice(a-minimum, b+1-minimum) for a, b in coords)] = onoff

print('Part 1:', state.sum())

split_lines = [
    set(),
    set(),
    set(),
]

def split(split_lines, axis, split_point):
    pos = bisect.bisect_left(split_lines, split_point)
    if pos == len(split_lines) or split_lines[pos] != split_point:
        split_lines[axis].add(pos, split_point)

for onoff, *coords in instructions:
    print(onoff, coords)
    for axis, (a, b) in enumerate(coords):
        split_lines[axis].add(a)
        split_lines[axis].add(b+1)

split_lines = [sorted(list(l)) for l in split_lines]

state = numpy.zeros(tuple(len(lines) for lines in split_lines), dtype=int)

for i, line in enumerate(split_lines):
    print('i', i, line)

for onoff, *coords in instructions:
    print('turn', onoff, coords)
    slices = []
    for axis, (a, b) in enumerate(coords):
        slices.append(slice(
            bisect.bisect_left(split_lines[axis], a),
            bisect.bisect_right(split_lines[axis], b),
        ))
    state[tuple(slices)] = onoff

def axis_index(index, axis):
    return (*([slice(None, None)] * axis), index, ...)

for axis in range(3):
    poss = split_lines[axis]
    for pos, (curr_line, next_line) in enumerate(zip(poss, poss[1:])):
        state[axis_index(pos, axis)] *= next_line - curr_line
        print('m', axis, pos, next_line, curr_line, '*', next_line - curr_line)

print('Part 2:', state.sum())
