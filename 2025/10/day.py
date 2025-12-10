from pprint import pp
import sys

import numpy
import scipy

# Hint taken: `scipy.optimize.milp`

# In hindsight, lists of bools would proably work better than integers of bits 

data = sys.stdin.read().splitlines()
print(data)

total_part1 = 0
total_part2 = 0
for line in data:
    lights_in, *buttons_in, joltage_in = line.split()
    lights = sum(1<<i if (c == '#') else 0 for i, c in enumerate(lights_in[1:-1]))
    buttons = []
    for b in buttons_in:
        buttons.append(sum(1<<int(n) for n in b[1:-1].split(',')))
    joltages = [int(n) for n in joltage_in[1:-1].split(',')]
    pp((bin(lights), [bin(b) for b in buttons], joltages))

    nums = list(range(2**len(buttons)))
    nums.sort(key=int.bit_count)
    for i, num in enumerate(nums):
        print(i, num, bin(num))
        lights_now = 0
        bit = 0
        bits = num
        while bits:
            if bits % 2:
                lights_now ^= buttons[bit]
            bit += 1
            bits //= 2
        if lights_now == lights:
            print(num.bit_count())
            total_part1 += num.bit_count()
            break

    weights = numpy.ones(len(buttons))
    factors = numpy.array([
        [(button>>i) % 2 for button in buttons]
        for i, j in enumerate(joltages)
    ])
    jolts = numpy.array(joltages)
    constraints = scipy.optimize.LinearConstraint(factors, jolts, jolts)
    print(weights)
    print(factors)
    print(constraints)
    res = scipy.optimize.milp(weights, constraints=constraints, integrality=1)
    print(res)
    total_part2 += round(res.x.sum())

print('*** part 1:', total_part1)
print('*** part 2:', total_part2)
