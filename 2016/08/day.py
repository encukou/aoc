import sys
import numpy

data = sys.stdin.read().strip().splitlines()

def solve(instructions, size=(6, 50)):
    lights = numpy.zeros(size, dtype=bool)

    def print_lights(lights):
        for row in lights:
            for col in row:
                if col:
                    print('\x1b[7m#\x1b[m', end='')
                else:
                    print('.', end='')
            print()

    for instruction in instructions:
        print(instruction)
        match instruction.split():
            case 'rect', dims:
                w, h = dims.split('x')
                lights[:int(h), :int(w)] = True
            case 'rotate', axis, index, 'by', amount:
                index = int(index.strip('xy='))
                amount = int(amount)
                if axis == 'column':
                    lights[:, index] = numpy.roll(lights[:, index], amount)
                elif axis == 'row':
                    lights[index] = numpy.roll(lights[index], amount)
                else:
                    raise ValueError(axis)
            case _:
                raise ValueError(instruction)
        print_lights(lights)
    return lights.sum()

example = """
rect 3x2
rotate column x=1 by 1
rotate row y=0 by 4
rotate column x=1 by 1
""".strip().splitlines()

assert solve(example, (3, 7)) == 6

print(f'*** part 1: {solve(data)}')
print(f'(part 2, see above)')
