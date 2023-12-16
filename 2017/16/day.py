import sys

data = sys.stdin.read().strip()
print(data)

def dance(start_pos, instructions):
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
        print(instruction, ''.join(positions))
    return ''.join(positions)

assert dance('abcde', 's1,x3/4,pe/b') == 'baedc'


start_pos = 'abcdefghijklmnop'
assert len(start_pos) == 16
print('*** part 1:', dance(start_pos, data))




print('*** part 2:', ...)
