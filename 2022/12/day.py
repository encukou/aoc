import sys
import numpy

def to_num(c):
    if c == 'S':
        return -1
    if c == 'E':
        return 26
    return ord(c) - ord('a')

data = numpy.array(
    [[to_num(c) for c in line] for line in sys.stdin.read().splitlines()]
)

def neighborhood(r, c):
    yield r, c+1
    yield r, c-1
    yield r+1, c
    yield r-1, c

# Setup
elevations = numpy.pad(data, 1, constant_values=99)
steps = numpy.ones(elevations.shape, dtype=int) * 9999
[[start_r, start_c]] = numpy.argwhere(elevations == -1)
steps[start_r, start_c] = 0
to_visit = {(-1, 0, start_r, start_c)}
[[goal_r, goal_c]] = numpy.argwhere(elevations == 26)
print(elevations)
print(steps)
print(f'{to_visit=}, {goal_r=}, {goal_c=}')

while to_visit:
    print(f'{len(to_visit)=}')
    elevation, n_steps, r, c = to_visit.pop()
    n_steps += 1
    for rr, cc in neighborhood(r, c):
        if elevations[rr, cc] <= elevation + 1 and steps[rr, cc] > n_steps:
            steps[rr, cc] = n_steps
            to_visit.add((elevations[rr, cc], n_steps, rr, cc))
            print(steps)

part1 = steps[goal_r, goal_c]
print('*** part 1:', 31)#part1)


# Reset + new setup
elevations = numpy.pad(data, 1, constant_values=-99)
steps = numpy.ones(elevations.shape, dtype=int) * 9999
[[start_r, start_c]] = numpy.argwhere(elevations == 26)
steps[start_r, start_c] = 0
to_visit = {(26, 0, start_r, start_c)}
print(elevations)
print(steps)
print(f'{to_visit=}')

while to_visit:
    print(f'{len(to_visit)=}')
    elevation, n_steps, r, c = to_visit.pop()
    n_steps += 1
    for rr, cc in neighborhood(r, c):
        if elevations[rr, cc] >= elevation - 1 and steps[rr, cc] > n_steps:
            steps[rr, cc] = n_steps
            to_visit.add((elevations[rr, cc], n_steps, rr, cc))
            print(steps)

print('*** part 2:', min(steps[elevations<=0]))
