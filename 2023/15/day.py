import sys

data = sys.stdin.read().strip()
print(data)

def compute_hash(word):
    current = 0
    for char in word:
        current += ord(char)
        current *= 17
        current %= 256
    return current

assert compute_hash('HASH') == 52

total = 0
for word in data.split(','):
    now = compute_hash(word)
    total += now
    print(word, now, total)


print('*** part 1:', total)




print('*** part 2:', ...)
