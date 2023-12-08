import sys
import re
import itertools
import math

MAP_RE = re.compile(r'(\w+) = \((\w+), (\w+)\)')

data = sys.stdin.read().splitlines()

def solve(data):
    print(data)
    instructions = data[0]
    assert not data[1]
    desert_map = {}
    for line in data[2:]:
        match = MAP_RE.match(line)
        desert_map[match[1]] = {'L': match[2], 'R': match[3]}
    return solve_maze(instructions, desert_map, 'AAA', (lambda c: c == 'ZZZ'))

def solve_maze(instructions, desert_map, start, check_end):
    current = start
    for turn_no, instruction in enumerate(itertools.cycle(instructions), start=1):
        entry = desert_map[current]
        print(turn_no, current, entry)
        current = entry[instruction]
        if check_end(current):
            print(turn_no)
            return turn_no

assert solve("""LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)
""".splitlines()) == 6

print('*** part 1:', solve(data))

def part2(data):
    print(data)
    instructions = data[0]
    assert not data[1]
    desert_map = {}
    for line in data[2:]:
        match = MAP_RE.match(line)
        desert_map[match[1]] = {'L': match[2], 'R': match[3]}
    lengths = []
    for start in (place for place in desert_map if place.endswith('A')):
        num_steps = solve_maze(instructions, desert_map, start, (lambda c: c.endswith('Z')))
        lengths.append(num_steps)
    print(lengths)
    return math.lcm(*lengths)


assert part2("""LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)
""".splitlines()) == 6


print('*** part 2:', part2(data))
