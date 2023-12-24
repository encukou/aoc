import sys
from dataclasses import dataclass
import itertools
from functools import cached_property
from sympy import solve, symbols, Eq

data = sys.stdin.read().splitlines()
print(data)

class Hailstone:
    pos: tuple
    velocity: tuple

    def __init__(self, line):
        pos_str, vel_str = line.split('@')
        self.pos = tuple(int(n) for n in pos_str.split(','))
        self.velocity = tuple(int(n) for n in vel_str.split(','))

    def __repr__(self):
        return f'<{self.pos} @ {self.velocity}>'

hailstones = []
for line in data:
    hailstones.append(Hailstone(line))

if len(data) < 20:
    test_range = 7, 27
else:
    test_range = 200000000000000, 400000000000000

intersections = []
count = 0
for a, b in itertools.combinations(hailstones, 2):
    print()
    print(a)
    print(b)
    x1, y1, _ = a.pos
    x2, y2, _ = (p+v for p, v in zip(a.pos, a.velocity))
    x3, y3, _ = b.pos
    x4, y4, _ = (p+v for p, v in zip(b.pos, b.velocity))
    den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if den == 0:
        print('parallel')
        continue
    px = (
        (x1*y2 - y1*x2) * (x3 - x4) - (x1 - x2) * (x3*y4 - y3*x4)
    ) / den
    py = (
        (x1*y2 - y1*x2) * (y3 - y4) - (y1 - y2) * (x3*y4 - y3*x4)
    ) / den
    is_inside = (
        test_range[0] <= px <= test_range[1]
        and test_range[0] <= py <= test_range[1]
    )
    for stone in (a, b):
        t = (px - stone.pos[0]) / stone.velocity[0]
        intersections.append((t, {a, b}, is_inside, (px, py)))
        if t < 0:
            print(f'in the past for {stone}')
            break
    else:
        if is_inside:
            print('in at', px, py)
            count += 1
        else:
            print('out at', px, py)

print('*** part 1:', count, flush=True)

equations = []
p_Rx, v_Rx = symbols('p_Rx v_Rx')
p_Ry, v_Ry = symbols('p_Ry v_Ry')
p_Rz, v_Rz = symbols('p_Rz v_Rz')
ts = []
for i, stone in enumerate(hailstones):
    p_Snx, v_Snx = stone.pos[0], stone.velocity[0]
    p_Sny, v_Sny = stone.pos[1], stone.velocity[1]
    p_Snz, v_Snz = stone.pos[2], stone.velocity[2]
    t_n = symbols(f't_{i}')
    equations.append(Eq(p_Rx + v_Rx * t_n, p_Snx + v_Snx * t_n))
    equations.append(Eq(p_Ry + v_Ry * t_n, p_Sny + v_Sny * t_n))
    equations.append(Eq(p_Rz + v_Rz * t_n, p_Snz + v_Snz * t_n))
    ts.append(t_n)
for equation in equations:
    print(equation)
# p_Rx + v_Rx t_n == p_Snx + v_Snx t_n
variables = [p_Rx, v_Rx, p_Ry, v_Ry, p_Rz, v_Rz] + ts
print(variables, flush=True)

# Solve the first 9. Ideally this needs an independence check...
solutions = solve(equations[:9], variables, dict=True)
print(solutions)
solution = solutions[0]
print(solution)

result = solution[p_Rx] + solution[p_Ry] + solution[p_Rz]

print('*** part 2:', result)
