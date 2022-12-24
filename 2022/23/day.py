import sys
from dataclasses import dataclass
from collections import namedtuple, Counter
from functools import cached_property
from itertools import count

data = sys.stdin.read().splitlines()
print(data)

WARMUP = """
.....
..##.
..#..
.....
..##.
.....
""".strip().splitlines()

def adjacent_directions(d):
    return d, d + d * 1j, d + d * -1j

CARDINAL_DIRECTIONS = -1, 1, -1j, 1j
EIGHT_NEIBORHOOD = frozenset().union(
    *(adjacent_directions(d) for d in CARDINAL_DIRECTIONS)
)


def get_char(direction):
    return {1j: '>', 1: 'v', -1j: '<', -1: '^', 0: '×'}.get(direction, '?')

def print_elves(elves):
    rs = set(e.real for e in elves)
    js = set(e.imag for e in elves)
    rrange = range(int(min(rs))-1, int(max(rs))+2)
    jrange = range(int(min(js))-1, int(max(js))+2)
    for r in rrange:
        for c in jrange:
            pos = r + c*1j
            if elf := elves.get(pos):
                if elf == '#':
                    print('\x1b[7m# \x1b[27m', end='')
                else:
                    print(f'\x1b[7m#{get_char(elf-pos)}\x1b[27m', end='')
            else:
                print('. ', end='')
        print()

def load_elves(data):
    elves = {}
    for r, line in enumerate(data):
        for c, char in enumerate(line):
            if char =='#':
                elves[r + 1j*c] = '#'
    return elves

def simulate(data, n_steps=None):
    elves = load_elves(data)
    directions = list(CARDINAL_DIRECTIONS)
    if n_steps is None:
        step_it = count()
    else:
        step_it = range(n_steps)
    for step_i in step_it:
        step_i += 1
        disp = {}
        num_unhappy = 0
        # elves: starting position of elf -> proposal
        # proposals: proposal -> starting position of proposing elf
        proposals = {}
        for pos in elves:
            if not any(pos+a in elves for a in EIGHT_NEIBORHOOD):
                proposed_pos = pos
            else:
                num_unhappy += 1
                for d in directions:
                    if not any(pos+a in elves for a in adjacent_directions(d)):
                        proposed_pos = pos+d
                        break
                else:
                    proposed_pos = pos
            if (conflicting_elf := proposals.get(proposed_pos)) is None:
                elves[pos] = proposed_pos
                proposals[proposed_pos] = pos
            else:
                # There's a conflict. Reset the conflicting elf so that its
                # proposal is its starting position.
                # The rules imply that no more than 2 elves can conflict,
                # so there's no need to mark the conflicting tile in case more
                # elves want to step there.
                elves[proposals.pop(proposed_pos)] = conflicting_elf
                proposals[conflicting_elf] = conflicting_elf
                # The current elf proposes its starting position, so it.
                # won't move.
                elves[pos] = pos
                proposals[pos] = pos
        if len(elves) < 20 or step_i % 17 == 0:
            print(f'{step_i}: {num_unhappy} elves wanna go {"".join(get_char(d) for d   in directions)}')
        if len(elves) < 20 or step_i % 100 == 0:
            print_elves(elves)
        elves = proposals
        if not num_unhappy:
            break
        directions.append(directions.pop(0))
    print(f'fini:')
    print_elves(elves)
    rs = set(e.real for e in elves)
    js = set(e.imag for e in elves)
    empty_in_rect = int((max(rs)-min(rs)+1) * (max(js)-min(js)+1)) - len(elves)
    return empty_in_rect, step_i

simulate(WARMUP, 4)

answer1, step_i = simulate(data, 10)
print('*** part 1:', answer1)

bignum, answer2 = simulate(data)
print('*** part 2:', answer2)
