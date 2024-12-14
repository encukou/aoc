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

recipes = [3, 7]
elves = [0, 1]
for i in range(target):
    for digit in str(sum(recipes[elf] for elf in elves)):
        recipes.append(int(digit))
    elves = [(elf + 1 + recipes[elf]) % len(recipes) for elf in elves]
    if len(recipes) < 20:
        print(i, elves, recipes)
    elif i % 100 == 0:
        print(i, elves, len(recipes))
    key = len(recipes)-10
    if key in checkpoints:
        score = ''.join(str(d) for d in recipes[key:len(recipes)])
        print(key, score)
        want = checkpoints[key]
        if want is None:
            print('*** part 1:', score)
            break
        else:
            assert score == want







print('*** part 2:', ...)
