import sys

data = sys.stdin.read().splitlines()
print(data)

def parse_range(x):
    start, stop = x.split('-')
    return set(range(int(start), int(stop)+1))

count = 0
for line in data:
    a, b = line.split(',')
    a  = parse_range(a)
    b  = parse_range(b)
    if a >= b or a <= b:
        count += 1

print('*** part 1:', count)




print('*** part 2:', ...)
