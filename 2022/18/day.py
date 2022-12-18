import sys
import collections

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




print('*** part 2:', ...)
