import sys
from itertools import count

data = sys.stdin.read().strip()
print(data)

def part1():
    banks = [int(b) for b in data.split()]
    seen = set()
    for turn in count(start=1):
        print(banks)

        hand = max(banks)
        idx = banks.index(hand)
        banks[idx] = 0
        for i in range(hand):
            idx += 1
            idx %= len(banks)
            banks[idx] += 1

        new = tuple(banks)
        if new in seen:
            return turn
        seen.add(new)


print('*** part 1:', part1())




print('*** part 2:', ...)
