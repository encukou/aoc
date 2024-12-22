import sys
import collections

data = sys.stdin.read().splitlines()
print(data)

"""

    Calculate the result of multiplying the secret number by 64. Then, mix this result into the secret number. Finally, prune the secret number.
    Calculate the result of dividing the secret number by 32. Round the result down to the nearest integer. Then, mix this result into the secret number. Finally, prune the secret number.
    Calculate the result of multiplying the secret number by 2048. Then, mix this result into the secret number. Finally, prune the secret number.

"""
def mix(base, other):
    return base ^ other
assert mix(42, 15) == 37

def prune(num):
    return num % 16777216
assert prune(100000000) == 16113920

def get_next(num):
    num = prune(mix(num, num * 64))
    num = prune(mix(num, num // 32))
    num = prune(mix(num, num * 2048))
    return num

num = 123
for example in """
    15887950
    16495136
    527345
    704524
    1553684
    12683156
    11100544
    12249484
    7753432
    5908254
""".strip().splitlines():
    num = get_next(num)
    print(num, example)
    assert num == int(example)

total = 0
for line in data:
    start = int(line)
    num = start
    for i in range(2000):
        num = get_next(num)
    total += num
    print(start, num, total)

print('*** part 1:', total)

if len(data) == 4:
    data = [1, 2, 3, 2024]

num = 123
for example in """
    3 (from 123)
    0 (from 15887950)
    6 (from 16495136)
    5 (etc.)
    4
    4
    6
    4
    4
    2
""".strip().splitlines():
    assert num % 10 == int(example.strip()[0])
    num = get_next(num)

sequences = collections.Counter()
for lineno, line in enumerate(data):
    seen = set()
    differences = collections.deque(maxlen=4)
    start = int(line)
    num = start
    for i in range(2000):
        next_num = get_next(num)
        diff = next_num%10 - num%10
        differences.append(diff)
        if len(differences) == 4:
            td = tuple(differences)
            #print(next_num, diff, td)
            if td not in seen:
                seen.add(td)
                sequences[td] += next_num%10
        num = next_num
    print(lineno, sequences.most_common(3), flush=True)
[(best_seq, num_bananas)] = sequences.most_common(1)
if len(data) == 4:
    print(f'{sequences[-2,1,-1,3]=}')

print('*** part 2:', num_bananas)
