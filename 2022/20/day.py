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

numbers = list(enumerate(int(line) for line in data))

if PRINTING and len(numbers) < 100:
    print('Initial arrangement:')
    print(*(n for i, n in numbers), sep=', ')
    print()
assert len(numbers) == len(set(numbers))
for idx_to_move in range(len(numbers)):
    for current_idx, (orig_idx, n) in enumerate(numbers):
        if orig_idx == idx_to_move:
            ins_idx = (current_idx + n) % (len(numbers)-1)
            if ins_idx == 0 and n < 0:
                ins_idx = len(numbers)-1
            del numbers[current_idx]
            numbers.insert(ins_idx, (orig_idx, n))
            if PRINTING:
                before = numbers[(ins_idx-1) % len(numbers)][1]
                after = numbers[(ins_idx+1) % len(numbers)][1]
                print(f'{n} moves between {before} and {after}:')
            if PRINTING and len(numbers) < 100:
                print(*(n for i, n in numbers), sep=', ')
                print()
            break

for i, (o, n) in enumerate(numbers):
    if n == 0:
        print(f'zero is in position {i}')
        parts = [
            numbers[(i+offset) % len(numbers)][1]
            for offset in (0, 1000, 2000, 3000)
        ]
        print('summing', parts)
        print('*** part 1:', sum(parts))
        break



print('*** part 2:', ...)
