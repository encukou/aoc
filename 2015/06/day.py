import sys
import numpy

data = sys.stdin.read().strip().splitlines()

lights = numpy.zeros((1000, 1000), dtype=bool)
for line in data:
    match line.split():
        case *instruction, xy1, 'through', xy2:
            x1, y1 = (int(n) for n in xy1.split(','))
            x2, y2 = (int(n)+1 for n in xy2.split(','))
            match instruction:
                case 'turn', 'on':
                    lights[x1:x2, y1:y2] = True
                case 'turn', 'off':
                    lights[x1:x2, y1:y2] = False
                case ['toggle']:
                    lights[x1:x2, y1:y2] = ~lights[x1:x2, y1:y2]
                case _:
                    raise ValueError(line)
        case _:
            raise ValueError(line.split())

print(f'*** part 1: {lights.sum()}')


lights = numpy.zeros((1000, 1000), dtype=int)
for line in data:
    match line.split():
        case *instruction, xy1, 'through', xy2:
            x1, y1 = (int(n) for n in xy1.split(','))
            x2, y2 = (int(n)+1 for n in xy2.split(','))
            match instruction:
                case 'turn', 'on':
                    lights[x1:x2, y1:y2] += 1
                case 'turn', 'off':
                    lights[x1:x2, y1:y2] -= 1
                    lights = lights.clip(0)
                case ['toggle']:
                    lights[x1:x2, y1:y2] += 2
                case _:
                    raise ValueError(line)
        case _:
            raise ValueError(line.split())

print(f'*** part 1: {lights.sum()}')
