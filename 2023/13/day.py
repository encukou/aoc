import sys
import numpy

data = [pat.splitlines() for pat in sys.stdin.read().split('\n\n')]
print(data)

def analyze(pattern, num_smudges):
    for r in range(1, pattern.shape[0]):
        print(r)
        a = pattern[r:]
        b = pattern[:r][::-1]
        m = min(len(a), len(b))
        a = a[:m]
        b = b[:m]
        #print(a)
        #print(b)
        if a.shape == b.shape and (a != b).sum() == num_smudges:
            yield r

def solve(num_smudges):
    total = 0
    for pattern in data:
        pattern = numpy.array([
            list(0 if c == '.' else 1 for c in row)
            for row in pattern
        ])
        print(pattern)
        new = (sum(analyze(pattern, num_smudges)) * 100
               + sum(analyze(pattern.T, num_smudges)))
        print(new, '->', total)
        total += new
    return total


print('*** part 1:', solve(0))
print('*** part 2:', solve(1))
