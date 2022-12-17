import sys
import numpy
import itertools

data = sys.stdin.read().strip()
jets = list(-1 if j == '<' else 1 for j in data)

NUM_ROCKS = 2022

T = True
F = False

rocks = [
    numpy.array([[T, T, T, T]]),
    numpy.array([[F, T, F],
                 [T, T, T],
                 [F, T, F]]),
    numpy.array([[F, F, T],
                 [F, F, T],
                 [T, T, T]]),
    numpy.array([[T],
                 [T],
                 [T],
                 [T]]),
    numpy.array([[T, T],
                 [T, T]]),
]
print(rocks)

MAT_SIZE = NUM_ROCKS*3
CHAMBER_WIDTH = 7

def logical_top_line(top_line):
    return MAT_SIZE - top_line - 1

def draw_chamber(chamber, top_line, test=None):
    if test is None:
        test = chamber
    for i in range(top_line-6, min(MAT_SIZE-1, top_line+17)):
        print(
            f'{i:4} |',
            *numpy.where(
                chamber[i, 1:-1],
                '██',
                numpy.where(test[i, 1:-1], '[]', '. '),
            ),
            '|',
            f' {logical_top_line(i):4}',
            ' (top)' if i == top_line else '',
            sep='',
        )
    print("     '--------------'")

chamber = numpy.zeros((MAT_SIZE, CHAMBER_WIDTH+2), dtype=bool)
chamber[..., 0] = True
chamber[..., -1] = True
chamber[-1] = True
top_line = MAT_SIZE-1
jet_iter = itertools.cycle(jets)
draw_chamber(chamber, top_line)
for num_rock, rock in zip(range(NUM_ROCKS), itertools.cycle(rocks)):
    log_line_by_line = num_rock < 3
    rock_pos = top_line - rock.shape[0] - 3, 3
    def pos():
        return (
            slice(rock_pos[0], rock_pos[0]+rock.shape[0]),
            slice(rock_pos[1], rock_pos[1]+rock.shape[1]),
        )
    def get_test(rock):
        test = numpy.zeros(chamber.shape, dtype=bool)
        test[pos()] = rock
        return test
    print(f'rock {num_rock} starts falling from {rock_pos}, top {top_line}')
    draw_chamber(chamber, top_line, get_test(rock))
    for gust in jet_iter:
        rock_pos = rock_pos[0], rock_pos[1] + gust
        test = get_test(rock)
        if (chamber & test).any():
            if log_line_by_line:
                print(f'gust push {gust} ineffective')
            rock_pos = rock_pos[0], rock_pos[1] - gust
        else:
            if log_line_by_line:
                print(f'gust push {gust} to {rock_pos}')
            if log_line_by_line:
                draw_chamber(chamber, top_line, test)

        rock_pos = rock_pos[0] + 1, rock_pos[1]
        test = get_test(rock)
        if (chamber & test).any():
            rock_pos = rock_pos[0] - 1, rock_pos[1]
            chamber[pos()] |= rock
            top_line = min(rock_pos[0], top_line)
            if log_line_by_line:
                print('rock rests')
                draw_chamber(chamber, top_line)
            break
        else:
            if log_line_by_line:
                print('rock falls')
                draw_chamber(chamber, top_line, test)

print('rocks fell')
draw_chamber(chamber, top_line)
print('*** part 1:', logical_top_line(top_line))




print('*** part 2:', ...)
