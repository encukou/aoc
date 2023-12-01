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


def valid2(phrase):
    words = [''.join(sorted(w)) for w in phrase.split()]
    return len(words) == len(set(words))

assert valid2('abcde fghij')
assert not valid2('abcde xyz ecdab')
assert valid2('a ab abc abd abf abj')
assert valid2('iiii oiii ooii oooi oooo')
assert not valid2('oiii ioii iioi iiio')



print('*** part 2:', sum(valid2(row) for row in data))
