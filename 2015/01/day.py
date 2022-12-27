import sys

data = sys.stdin.read()

print('*** part 1:', data.count('(') - data.count(')'))

floor = 0
for i, char in enumerate(data):
    floor -= '(-)'.index(char) - 1
    if floor < 0:
        print('*** part 2:', i+1)
        break
