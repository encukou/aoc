import sys
from math import prod

data = sys.stdin.read().splitlines()
print(data)

results = []
for time, record in zip(*([int(n) for n in line.split(':')[-1].split()] for line in data)):
    print(time, record)
    ways = 0
    for held in range(time):
        released = time - held
        distance = held * released
        print(held, released, distance)
        if distance > record:
            ways += 1
    if ways:
        results.append(ways)
print(results)

print('*** part 1:', prod(results))




print('*** part 2:', ...)
