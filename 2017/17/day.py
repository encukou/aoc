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




print('*** part 2:', ...)
