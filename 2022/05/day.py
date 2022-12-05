import sys
import re

data = sys.stdin.read().splitlines()

MOVE_RE = re.compile(r'move (\d+) from (\d+) to (\d+)')

def format_stacks(stacks):
    """Format stacks for nicer display"""
    return ''.join('[' + ''.join(s) + ']' for s in stacks)

def solve(part_num):
    stacks = []
    for line in data:
        if not line.startswith('move'):
            if not line.strip().startswith('1'):
                # Build the stacks line by line (top to bottom)
                # Letters apear in positions 1, 5, 9, ...
                for stack_num, letter in enumerate(line[1::4]):
                    if letter == ' ':
                        continue
                    while len(stacks) <= stack_num:
                        stacks.append([])
                    stacks[stack_num].append(letter)
                    print(f"{letter} to {stack_num}: {format_stacks(stacks)}")
            else:
                # Stacks are built. Reverse them (bottom to top), so
                # pop()/append(), which work on the end of the list, simulate
                # the crane.
                print('Reverse stacks')
                for stack in stacks:
                    stack.reverse()
                print(format_stacks(stacks))
        elif line.strip():
            # Parse 'move' line
            amt, src, dst = MOVE_RE.match(line).groups()
            amt = int(amt)
            src = int(src) - 1
            dst = int(dst) - 1
            print(f'move {amt} from {src} to {dst}')
            if part_num == 1:
                # pop/append N times
                for n in range(amt):
                    stacks[dst].append(stacks[src].pop())
            elif part_num == 2:
                # move whole sublist at once
                stacks[dst].extend(stacks[src][-amt:])
                del stacks[src][-amt:]
            print(format_stacks(stacks))
    # Return only the top crate of each stack
    return ''.join(s[-1] for s in stacks)

print('*** part 1:', solve(1))
print('*** part 2:', solve(2))
