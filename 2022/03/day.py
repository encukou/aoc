import sys

data = sys.stdin.read().splitlines()
print(data)


def get_score(letter):
    if letter.islower():
        return ord(letter) - ord('a') + 1
    return ord(letter) - ord('A') + 27

score = 0
for line in data:
    half1 = line[:len(line)//2]
    half2 = line[len(line)//2:]
    [common] = set(half1) & set(half2)
    print(common)
    score += get_score(common)


print('*** part 1:', score)




print('*** part 2:', ...)
