import sys

data = sys.stdin.read().splitlines()

PRINTING = True

def abs_sgn(x):
    if x > 0:
        return x, 1
    if x < 0:
        return -x, -1
    return 0, 0

def sgn(x):
    if x > 0:
        return 1
    if x < 0:
        return -1
    return 0

def solve(key, rounds):
    numbers = list(enumerate(int(line) * key for line in data))

    if PRINTING and len(numbers) < 100:
        print('Initial arrangement:')
        print(*(n for i, n in numbers), sep=', ')
        print()
    assert len(numbers) == len(set(numbers))
    for round_no in range(rounds):
        for idx_to_move in range(len(numbers)):
            for current_idx, (orig_idx, n) in enumerate(numbers):
                if orig_idx == idx_to_move:
                    ins_idx = (current_idx + n) % (len(numbers)-1)
                    if ins_idx == 0 and n < 0:
                        ins_idx = len(numbers)-1
                    del numbers[current_idx]
                    numbers.insert(ins_idx, (orig_idx, n))
                    if PRINTING and rounds <= 1:
                        if n == 0:
                            print('0 does not move:')
                        else:
                            before = numbers[(ins_idx-1) % len(numbers)][1]
                            after = numbers[(ins_idx+1) % len(numbers)][1]
                            print(f'{n} moves between {before} and {after}:')
                    if PRINTING and rounds <= 1 and len(numbers) < 100:
                        print(*(n for i, n in numbers), sep=', ')
                        print()
                    break
        if PRINTING:
            for i, (o, n) in enumerate(numbers):
                if n == 0:
                    numbers = numbers[i:] + numbers[:i]
            print(f'After {round_no+1} round{"s"*bool(round_no)} of mixing:')
            print(*(n for i, n in numbers), sep=', ')

    for i, (o, n) in enumerate(numbers):
        if n == 0:
            print(f'zero is in position {i}')
            parts = [
                numbers[(i+offset) % len(numbers)][1]
                for offset in (0, 1000, 2000, 3000)
            ]
            print('summing', parts)
            return sum(parts)

print('*** part 1:', solve(1, 1))


print('*** part 2:', solve(811589153, 10))
