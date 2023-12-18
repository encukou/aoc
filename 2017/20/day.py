import sys
import re
import collections

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

num_escaped = 0
particles = []
for i, line in enumerate(data):
    particles.append(tuple([*(int(n) for n in PARTICLE_RE.findall(line)), i]))
while True:
    collision_counter = collections.Counter(p[:3] for p in particles)
    print(f'{len(particles)} before collisions')
    particles = [p for p in particles if collision_counter[p[:3]] == 1]
    if not particles:
        break
    print(f'{len(particles)} left after collisions')
    mins = tuple(min(p[i] for p in particles) for i in range(9))
    maxs = tuple(max(p[i] for p in particles) for i in range(9))
    print(mins, maxs)
    new_particles = []
    for px, py, pz, vx, vy, vz, ax, ay, az, n in particles:
        if (px, vx, ax) == mins[0::3]:
            print(f'particle {n} flies away in -x')
            num_escaped += 1
        elif (py, vy, ay) == mins[1::3]:
            print(f'particle {n} flies away in -y')
            num_escaped += 1
        elif (pz, vz, az) == mins[2::3]:
            print(f'particle {n} flies away in -z')
            num_escaped += 1
        elif (px, vx, ax) == maxs[0::3]:
            print(f'particle {n} flies away in +x')
            num_escaped += 1
        elif (py, vy, ay) == maxs[1::3]:
            print(f'particle {n} flies away in +y')
            num_escaped += 1
        elif (pz, vz, az) == maxs[2::3]:
            print(f'particle {n} flies away in +z')
            num_escaped += 1
        else:
            vx += ax
            vy += ay
            vz += az
            px += vx
            py += vy
            pz += vz
            new_particles.append((px, py, pz, vx, vy, vz, ax, ay, az, n))
    particles = new_particles


print('*** part 2:', num_escaped)
