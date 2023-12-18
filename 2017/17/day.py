import sys

data = sys.stdin.read().strip()
print(data)

step = int(data)
buf = [0]
pos = 0
for i in range(1, 2017+1):
    pos += step
    pos %= len(buf)
    pos += 1
    buf.insert(pos, i)
    if len(buf) < 10:
        print(buf)


print('*** part 1:', buf[(pos+1) % len(buf)])

bufsize = 1
pos = 0
after_zero = None
for i in range(1, 50000000+1):
    pos += step
    pos %= bufsize
    pos += 1
    bufsize += 1
    if pos == 1:
        after_zero = i
    if i % 50007 == 0:
        print(f'{i=} {pos=} +{step} {bufsize=}')

print('*** part 2:', after_zero)
