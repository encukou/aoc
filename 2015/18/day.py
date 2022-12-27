import sys
import numpy
import scipy

data = sys.stdin.read().strip().splitlines()

ENCODING = {'#': 1, '.': 0}
NUM_STEPS = 100 if len(data) > 10 else 4

orig_lights = numpy.array([[ENCODING[c] for c in line] for line in data])

def print_lights(lights):
    for row in lights:
        for val in row:
            if val:
                print('#', end='')
            else:
                print('.', end='')
        print()

print_lights(orig_lights)

transitions_from_off = [False] * 9
transitions_from_off[3] = True
transitions_from_on = [False] * 9
transitions_from_on[2] = True
transitions_from_on[3] = True
TRANSITIONS = transitions_from_off + transitions_from_on

KERNEL = numpy.array([
    [1, 1, 1],
    [1, 9, 1],
    [1, 1, 1],
])

def do_step(lights):
    return numpy.choose(
        scipy.signal.convolve(lights, KERNEL, mode='same'),
        TRANSITIONS,
    )

lights = orig_lights
for step_num in range(1, NUM_STEPS+1):
    lights = do_step(lights)
    print(f'After step {step_num}:')
    print_lights(lights)

print(f'*** part 1: {lights.sum()}')

lights = orig_lights
lights[0, 0] = lights[0, -1] = lights[-1, 0] = lights[-1, -1] = 1
for step_num in range(1, NUM_STEPS+1):
    lights = do_step(lights)
    lights[0, 0] = lights[0, -1] = lights[-1, 0] = lights[-1, -1] = 1
    print(f'After step {step_num}:')
    print_lights(lights)

print(f'*** part 2: {lights.sum()}')
