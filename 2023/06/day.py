import sys
from math import prod

data = sys.stdin.read().splitlines()
print(data)

def solve(time, record):
    print('---', time, record)
    def beats(held):
        released = time - held
        distance = held * released
        return distance > record
    low, high = 0, time // 2
    while low != high - 1:
        mid = (low + high) // 2
        if beats(mid):
            high = mid
        else:
            low = mid
        print([low, high])
    return time - 2 * low - 1

results = [solve(time, record) for time, record in zip(*([int(n) for n in line.split(':')[-1].split()] for line in data))]
print(results)

print('*** part 1:', prod(results))

result = solve(*[int(line.split(':')[-1].replace(' ', '')) for line in data])

print('*** part 2:', result)
