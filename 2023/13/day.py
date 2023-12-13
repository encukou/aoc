import sys
import numpy

data = [pat.splitlines() for pat in sys.stdin.read().split('\n\n')]
print(data)

def analyze(pattern):
    for r in range(1, pattern.shape[0]):
        print(r)
        a = pattern[r:]
        b = pattern[:r][::-1]
        m = min(len(a), len(b))
        a = a[:m]
        b = b[:m]
        print(a)
        print(b)
        if a.shape == b.shape and (a == b).all():
            yield r

total = 0
for pattern in data:
    pattern = numpy.array([list(0 if c == '.' else 1 for c in row) for row in pattern])
    print(pattern)
    new = 100 * sum(analyze(pattern)) + sum(analyze(pattern.T))
    print(new, '->', total)
    total += new


print('*** part 1:', total)




print('*** part 2:', ...)
