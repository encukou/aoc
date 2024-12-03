from collections import Counter
import sys

data = sys.stdin.read().splitlines()
print(data)

twos = 0
threes = 0
for box in data:
    counter = Counter(box)
    if 2 in counter.values():
        twos += 1
    if 3 in counter.values():
        threes += 1

print('*** part 1:', twos * threes)




print('*** part 2:', ...)
