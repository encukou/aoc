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

def find_common_letters(boxes):
    looking_for = set()
    for box in data:
        print(box)
        for i in range(len(box) - 1):
            key = box[:i] + box[i + 1:], i
            if key in looking_for:
                return key[0]
            looking_for.add(key)


print('*** part 2:', find_common_letters(data))
