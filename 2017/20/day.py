import sys
import re

data = sys.stdin.read().splitlines()
print(data)

PARTICLE_RE = re.compile('([-\d]+)')

def manh(x, y, z):
    return abs(x) + abs(y) + abs(z)

particles = []
for i, line in enumerate(data):
    px, py, pz, vx, vy, vz, ax, ay, az = (
        int(n) for n in PARTICLE_RE.findall(line)
    )
    particles.append((manh(ax, ay, az), manh(vx, vy, vz), manh(px, py, pz), i))
particles.sort()


print('*** part 1:', particles[0][-1])
# 504 too high



print('*** part 2:', ...)
