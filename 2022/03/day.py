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
    print(common, get_score(common))
    score += get_score(common)


print('*** part 1:', score)

score = 0
for l0, l1, l2 in zip(data[0::3], data[1::3], data[2::3]):
    [common] = set(l0) & set(l1) & set(l2)
    print(common, get_score(common))
    score += get_score(common)


print('*** part 2:', score)
