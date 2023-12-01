import sys

data = sys.stdin.read().splitlines()
print(data)

def valid(phrase):
    words = phrase.split()
    return len(words) == len(set(words))

assert valid('aa bb cc dd ee')
assert not valid('aa bb cc dd aa')
assert valid('aa bb cc dd aaa')


print('*** part 1:', sum(valid(row) for row in data))




print('*** part 2:', ...)
