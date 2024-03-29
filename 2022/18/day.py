import sys
import collections

import numpy

data = sys.stdin.read().splitlines()

def get_cube_faces(x, y, z):
    """A cube face is represented by its orientation and starting point.

    For example face ('xy', x, y, z) stretches between these points:
    - x, y,   z
    - x, y+1, z
    - x, y,   z+1
    - x, y+1, z+1
    """
    yield 'xy',  x,   y,   z
    yield 'xy',  x,   y,   z+1

    yield 'yz',  x,   y,   z
    yield 'yz',  x+1, y,   z

    yield 'xz',  x,   y,   z
    yield 'xz',  x,   y+1, z

def count_boundary_faces(cubes):
    face_counter = collections.Counter()
    for cube in list(cubes):
        for face in get_cube_faces(*cube):
            face_counter[face] += 1

    # Only count faces that aren't duplicated
    num_singles = 0
    for face, count in face_counter.items():
        if count == 1:
            num_singles += 1
    return num_singles

cubes = [
    tuple(int(c) for c in line.split(','))
    for line in data
]
num_boundary_faces = count_boundary_faces(cubes)

print('*** part 1:', num_boundary_faces)

numpy.set_printoptions(threshold=sys.maxsize, formatter={'numpystr':str})
# Get a big enough NumPy array
xs = [x for x, y, z in cubes]
ys = [y for x, y, z in cubes]
zs = [z for x, y, z in cubes]
space = numpy.zeros((max(xs)+1, max(ys)+1, max(zs)+1), dtype=numpy.uint8)

# The meaning of entries in the array:
UNKNOWN = 0
ROCK = 1
PADDING = 2
STEAM = 3

for cube in cubes:
    space[cube] = ROCK

# Pad the array with UNKNOWN and PADDING
space = numpy.pad(space, 1, constant_values=UNKNOWN)
space = numpy.pad(space, 1, constant_values=PADDING)

# Flood fill UNKNOWN with STEAM, starting in one corner
frontier = {(1, 1, 1)}
while frontier:
    cube = frontier.pop()
    if space[cube] == UNKNOWN:
        space[cube] = STEAM
        x, y, z = cube
        frontier.update((
            (x+1, y, z),
            (x-1, y, z),
            (x, y+1, z),
            (x, y-1, z),
            (x, y, z+1),
            (x, y, z-1),
        ))

# Print out...
for n, plane in enumerate(space):
    print(f'plane {n}:')
    for line in plane:
        for elem in line:
            print('▓█▒░'[elem]*2, end='')
        print()

# Process individual ROCK/UNKNOWN cubes as in part 1
cubes = zip(*(space <= ROCK).nonzero())
num_boundary_faces = count_boundary_faces(cubes)

print('*** part 2:', num_boundary_faces)
