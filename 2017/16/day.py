import sys

data = sys.stdin.read().strip()
print(data)

def dance(start_pos, instructions, verbose=True):
    positions = list(start_pos)
    for instruction in instructions.split(','):
        if instruction.startswith('s'):
            split = int(instruction[1:])
            a, b = positions[:-split], positions[-split:]
            positions = b + a
        elif instruction.startswith('x'):
            a, b = instruction[1:].split('/')
            a = int(a)
            b = int(b)
            positions[a], positions[b] = positions[b], positions[a]
        elif instruction.startswith('p'):
            a, b = instruction[1:].split('/')
            a = positions.index(a)
            b = positions.index(b)
            positions[a], positions[b] = positions[b], positions[a]
        else:
            raise ValueError(instruction)
        if verbose:
            print(instruction, ''.join(positions))
    return ''.join(positions)

assert dance('abcde', 's1,x3/4,pe/b') == 'baedc'


if len(data) < 50:
    start_pos = 'abcde'
else:
    start_pos = 'abcdefghijklmnop'
    assert len(start_pos) == 16
print('*** part 1:', dance(start_pos, data))

NUM_DANCES = 1000000000
positions = start_pos
seen = {}
for n in range(NUM_DANCES):
    print(n, positions)
    if positions in seen:
        break
    seen[positions] = n
    positions = dance(positions, data, verbose=False)
loop_size = n - seen[positions]
remaining = NUM_DANCES - n
loops = remaining // loop_size
n += loop_size * loops
print(f'{loop_size=} {remaining=} {loops=} {n=}')
for n in range(n, NUM_DANCES):
    print(n, positions)
    positions = dance(positions, data, verbose=False)


print('*** part 2:', positions)
