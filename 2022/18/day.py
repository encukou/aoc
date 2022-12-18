import sys
import collections
import numpy

data = sys.stdin.read().splitlines()

def get_cube_faces(x, y, z):
    # xy
    yield frozenset([(x, y, z), (x, y+1, z), (x+1, y+1, z), (x+1, y, z)])
    yield frozenset([(x, y, z+1), (x, y+1, z+1), (x+1, y+1, z+1), (x+1, y, z+1)])
    # yz
    yield frozenset([(x, y, z), (x, y+1, z), (x, y+1, z+1), (x, y, z+1)])
    yield frozenset([(x+1, y, z), (x+1, y+1, z), (x+1, y+1, z+1), (x+1, y, z+1)])
    # xz
    yield frozenset([(x, y, z), (x+1, y, z), (x+1, y, z+1), (x, y, z+1)])
    yield frozenset([(x, y+1, z), (x+1, y+1, z), (x+1, y+1, z+1), (x, y+1, z+1)])

face_counter = collections.Counter()
for line in data:
    for face in get_cube_faces(*(int(c) for c in line.split(','))):
        face_counter[face] += 1

num_singles = 0
for face, count in face_counter.items():
    print(face, count)
    if count == 1:
        num_singles += 1

print('*** part 1:', num_singles)

numpy.set_printoptions(threshold=10000)
cubes = [tuple(int(c) for c in line.split(',')) for line in data]
assert (0, 0, 0) not in cubes
xs = [z for x, y, z in cubes]
ys = [z for x, y, z in cubes]
zs = [z for x, y, z in cubes]

space = numpy.zeros((max(xs)+1, max(ys)+1, max(zs)+1), dtype=numpy.uint8)
for cube in cubes:
    space[cube] = 1
space = numpy.pad(space, 1, constant_values=2)
print(space)
frontier = {(1, 1, 1)}
while frontier:
    cube = frontier.pop()
    if space[cube] == 0:
        space[cube] = 3
        print(space)
        x, y, z = cube
        frontier.update((
            (x+1, y, z),
            (x-1, y, z),
            (x, y+1, z),
            (x, y-1, z),
            (x, y, z+1),
            (x, y, z-1),
        ))
print((space <= 1).nonzero())
print(list(zip(*(space <= 1).nonzero())))

face_counter = collections.Counter()
for cube in list(zip(*(space <= 1).nonzero())):
    for face in get_cube_faces(*cube):
        face_counter[face] += 1

num_singles = 0
for face, count in face_counter.items():
    print(face, count)
    if count == 1:
        num_singles += 1

print('*** part 2:', num_singles)
# not 2056
