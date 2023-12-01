import sys
from itertools import count

data = sys.stdin.read().strip()
print(data)

def solve(banks):
    banks = list(banks)
    seen = set()
    for turn in count():
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
            return turn, banks
        seen.add(new)


part1, new_state = solve([int(b) for b in data.split()])
print('*** part 1:', part1+1)




part2, _ = solve(new_state)
print('*** part 2:', part2)
