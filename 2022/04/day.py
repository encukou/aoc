import sys

data = sys.stdin.read().splitlines()

def parse_range(x):
    start, stop = x.split('-')
    return set(range(int(start), int(stop)+1))

count1 = 0
count2 = 0
for line in data:
    a, b = line.split(',')
    a  = parse_range(a)
    b  = parse_range(b)
    if a >= b or a <= b:
        count1 += 1
    if a & b:
        count2 += 1

print('*** part 1:', count1)
print('*** part 2:', count2)
