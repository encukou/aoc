import collections
import time
import sys

data = sys.stdin.read().split()
print(data)

stones = {int(n): 1 for n in data}
def solve(stones, n_turns):
    this_time = time.time()
    for i in range(n_turns):
        new_stones = collections.defaultdict(int)
        for stone, amount in stones.items():
            s = str(stone)
            if stone == 0:
                new_stones[1] += amount
            elif len(s) % 2 == 0:
                new_stones[int(s[len(s) // 2:])] += amount
                new_stones[int(s[:len(s) // 2])] += amount
            else:
                new_stones[stone * 2024] += amount
        stones = new_stones

        last_time = this_time
        this_time = time.time()
        if len(stones) < 10:
            print(i, sum(stones.values()), stones)
        else:
            print(i, sum(stones.values()), round(this_time - last_time, 1), flush=True)
    return sum(stones.values())

print('*** part 1:', solve(stones, 25))
print('*** part 2:', solve(stones, 75))
