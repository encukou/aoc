import sys

data = sys.stdin.read().strip()
print(data)
if not data:
    print('no data')
    exit()

target = int(data)
checkpoints = {
    9: '5158916779',
    5: '0124515891',
    18: '9251071085',
    2018: '5941429882',
    target: None,
}

checkpoints_2 = (
    ([5, 1, 5, 8, 9], 9),
    ([0, 1, 2, 4, 5], 5),
    ([9, 2, 5, 1, 0], 18),
    ([5, 9, 4, 1, 4], 2018),
    (list(int(d) for d in data), None),
)


recipes = [3, 7]
elves = [0, 1]
parts = {1, 2}
i = 0
while True:
    i += 1
    for digit in str(sum(recipes[elf] for elf in elves)):
        recipes.append(int(digit))
        for key, want in checkpoints_2:
            if recipes[-len(key):] == key:
                checkpoints_2 = [(k, w) for k, w in checkpoints_2 if k != key]
                got = len(recipes) - len(key)
                if want:
                    assert got == want
                else:
                    if 2 in parts:
                        print('*** part 2:', got)
                        parts.discard(2)
    elves = [(elf + 1 + recipes[elf]) % len(recipes) for elf in elves]
    if len(recipes) < 20:
        print(i, elves, recipes)
    elif i % 1000 == 0:
        print(i, elves, len(recipes), len(checkpoints_2), parts)
    key = len(recipes)-10
    if key in checkpoints:
        score = ''.join(str(d) for d in recipes[key:len(recipes)])
        print(key, score)
        want = checkpoints[key]
        if want is None:
            if 1 in parts:
                print('*** part 1:', score)
                parts.discard(1)
        else:
            assert score == want
    if not parts:
        break
