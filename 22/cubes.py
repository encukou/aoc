import re

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
            (int(match[2])-minimum, int(match[3])-minimum),
            (int(match[4])-minimum, int(match[5])-minimum),
            (int(match[6])-minimum, int(match[7])-minimum),
        ))

state = numpy.zeros(
    (maximum-minimum, maximum-minimum, maximum-minimum),
    dtype=int,
)
print(state.shape)

for onoff, *coords in instructions:
    for a, b in coords:
        assert a<=b
    state[tuple(slice(a, b+1) for a, b in coords)] = onoff

print('Part 1:', state.sum())
# 590784
