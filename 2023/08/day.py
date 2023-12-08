import sys
import re
import itertools

MAP_RE = re.compile(r'([A-Z]+) = \(([A-Z]+), ([A-Z]+)\)')

data = sys.stdin.read().splitlines()

def solve(data):
    print(data)
    instructions = data[0]
    assert not data[1]
    desert_map = {}
    for line in data[2:]:
        match = MAP_RE.match(line)
        desert_map[match[1]] = {'L': match[2], 'R': match[3]}

    current = 'AAA'
    for turn_no, instruction in enumerate(itertools.cycle(instructions), start=1):
        entry = desert_map[current]
        print(turn_no, current, entry)
        current = entry[instruction]
        if current == 'ZZZ':
            print(turn_no)
            return turn_no

assert solve("""LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)
""".splitlines()) == 6

print('*** part 1:', solve(data))




print('*** part 2:', ...)
