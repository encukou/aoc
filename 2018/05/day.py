import sys

data = list(sys.stdin.read().strip())
print(''.join(data))

changed = True
while changed:
    changed = False
    for i in range(len(data) - 1, 0, -1):
        char = data[i]
        opposite = char.upper() if char.islower() else char.lower()
        print(char, data[i-1], opposite)
        if data[i-1] == opposite:
            del data[i-1:i+1]
            changed = True
            print(len(data))
    print(''.join(data))


print('*** part 1:', len(data))




print('*** part 2:', ...)
