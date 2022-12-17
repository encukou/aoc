import sys
import numpy
import itertools

data = sys.stdin.read().strip()
jets = list((n, -1 if j == '<' else 1) for n, j in enumerate(data))

CONTEXT_SIZE = 8

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

MAT_SIZE = 500  # (adjust in trouble)
CHAMBER_WIDTH = 7

def logical_top_line(top_line, top_line_offset):
    return top_line_offset - top_line

def draw_chamber(chamber, top_line, top_line_offset, test=None):
    if test is None:
        test = chamber
    for i in range(top_line-6, min(MAT_SIZE, top_line+100)):
        print(
            f'{i:4} |',
            *numpy.where(
                chamber[i, 1:-1],
                '██',
                numpy.where(test[i, 1:-1], '[]', '. '),
            ),
            '|',
            f' - line {logical_top_line(i, top_line_offset):4}',
            ' (top)' if i == top_line else '',
            sep='',
        )

def make_chamber():
    chamber = numpy.zeros((MAT_SIZE, CHAMBER_WIDTH+2), dtype=bool)
    chamber[..., 0] = True
    chamber[..., -1] = True
    chamber[-1] = True
    return chamber

def solve(rocks_total):
    chamber = make_chamber()
    top_line = MAT_SIZE-1
    top_line_offset = top_line
    jet_iter = itertools.cycle(jets)
    draw_chamber(chamber, top_line, top_line_offset)
    memo = {}
    rock_num = -1
    use_memo = True
    for rock_type, rock in itertools.cycle(enumerate(rocks)):
        rock_num += 1
        if rock_num == rocks_total:
            print(f'{rock_num} rocks fell')
            draw_chamber(chamber, top_line, top_line_offset)
            return logical_top_line(top_line, top_line_offset)

        log_line_by_line = rock_num < 3
        log_rock_by_rock = rock_num < 10
        log_context_clear_details = rock_num < 100
        log_context_clears = rock_num < 2000
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

        if log_rock_by_rock:
            draw_chamber(chamber, top_line, top_line_offset, get_test(rock))
        for gust_index, gust in jet_iter:
            if log_rock_by_rock:
                print(f'rock {rock_num} starts falling, {gust_index=}')
                log_rock_by_rock = False
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
                    draw_chamber(chamber, top_line, top_line_offset, test)

            rock_pos = rock_pos[0] + 1, rock_pos[1]
            test = get_test(rock)
            if (chamber & test).any():
                rock_pos = rock_pos[0] - 1, rock_pos[1]
                chamber[pos()] |= rock
                top_line = min(rock_pos[0], top_line)
                if log_line_by_line:
                    print('rock rests')
                    draw_chamber(chamber, top_line, top_line_offset)
                break
            else:
                if log_line_by_line:
                    print('rock falls')
                    draw_chamber(chamber, top_line, top_line_offset, test)

        if top_line < MAT_SIZE - CONTEXT_SIZE:
            context = chamber[top_line:top_line+CONTEXT_SIZE]
            if not context.any(axis=0).all():
                continue
            info = rock_type, gust_index, *numpy.packbits(context)
            prev_top = logical_top_line(top_line, top_line_offset)
            if log_context_clears:
                print(f'CONTEXT CLEAR @ {rock_num} ({top_line}): {info}')
            if log_context_clear_details:
                draw_chamber(chamber, top_line, top_line_offset)
            new_chamber = make_chamber()
            new_chamber[MAT_SIZE-CONTEXT_SIZE:] = context
            chamber = new_chamber
            delta = top_line - (MAT_SIZE - CONTEXT_SIZE)
            top_line_offset -= delta
            top_line -= delta
            if log_context_clear_details:
                print('to:')
                draw_chamber(chamber, top_line, top_line_offset)
            assert logical_top_line(top_line, top_line_offset) == prev_top
            if use_memo and info in memo:
                old_rock_num, old_top, old_offset = memo[info]
                assert old_top == top_line
                step = rock_num - old_rock_num
                offset_step = top_line_offset - old_offset
                print(f'{rock_num} repeats {old_rock_num}')
                print(f'{info=}:{memo[info]}, {step=} {offset_step=}')
                for scale_shift in reversed(range(rocks_total.bit_length())):
                    scale = 1 << scale_shift
                    bigstep = step * scale
                    bigoffsetstep = offset_step * scale
                    while rock_num + bigstep < rocks_total:
                        rock_num += bigstep
                        top_line_offset += bigoffsetstep
                        print(f'ffwd {scale:10}×{step} rocks to {rock_num}')
                use_memo = False
            else:
                memo[info] = rock_num, top_line, top_line_offset

print('*** part 1:', solve(2022))
print('*** part 2:', solve(1_000_000_000_000))
