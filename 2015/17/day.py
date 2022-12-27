import sys
from collections import Counter
from itertools import chain, combinations

data = sys.stdin.read().strip().splitlines()

AMOUNT = 150 if len(data) > 5 else 25
input_sizes = [int(n) for n in data]

num_possibilities = 0
possibilities_by_number = Counter()
for sizes in chain(*(
    combinations(input_sizes, r)
    for r in range(1, len(input_sizes))
)):
    if sum(sizes) == AMOUNT:
        print(sizes, sep='+')
        num_possibilities += 1
        possibilities_by_number[len(sizes)] += 1

print(f'*** part 1: {num_possibilities}')
print(f'*** part 2: {min(possibilities_by_number.items())[1]}')
