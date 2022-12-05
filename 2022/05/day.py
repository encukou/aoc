import sys
import re

data = sys.stdin.read().splitlines()

MOVE_RE = re.compile(r'move (\d+) from (\d+) to (\d+)')

stacks = []

moving = False
for line in data:
    if not moving:
        if line.strip().startswith('1'):
            moving = True
            for stack in stacks:
                stack.reverse()
            print([''.join(s) for s in stacks])
            continue
        for stack_num, letter in enumerate(line[1::4]):
            if letter == ' ':
                continue
            while len(stacks) <= stack_num:
                stacks.append([])
            print(stacks, stack_num, letter)
            stacks[stack_num].append(letter)
    elif line.strip():
        amt, src, dst = MOVE_RE.match(line).groups()
        amt = int(amt)
        src = int(src) - 1
        dst = int(dst) - 1
        print(f'move {amt} from {src} to {dst}')
        for n in range(amt):
            stacks[dst].append(stacks[src].pop())
        print([''.join(s) for s in stacks])


print('*** part 1:', ''.join(s[-1] for s in stacks))




print('*** part 2:', ...)
