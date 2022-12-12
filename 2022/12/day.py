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
data = numpy.pad(data, 1, constant_values=99)
print(data)

steps = numpy.ones(data.shape, dtype=int) * 9999
steps[data==-1] = 0

def around(r, c):
    yield r, c+1
    yield r, c-1
    yield r+1, c
    yield r-1, c

print(steps)
to_visit = set((-1, int(r), int(c)) for r, c in around(*numpy.where(steps==0)))
r, c = numpy.where(steps==0)
to_visit = {(-1, 0, int(r), int(c))}
goal_r, goal_c = numpy.where(data==26)
print(to_visit, goal_r, goal_c)

while to_visit:
    elevation, n_steps, r, c = to_visit.pop()
    n_steps += 1
    for rr, cc in around(r, c):
        if data[rr, cc] <= elevation + 1 and steps[rr, cc] > n_steps:
            steps[rr, cc] = n_steps
            to_visit.add((data[rr, cc], n_steps, rr, cc))
            print(steps)

[part1] = steps[goal_r, goal_c]
print('*** part 1:', part1)




print('*** part 2:', ...)
