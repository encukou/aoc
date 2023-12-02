import sys
import re
import operator
import functools

data = sys.stdin.read().splitlines()
print(data)

MAX = {
    'red': 12,
    'green': 13,
    'blue': 14,
}
print('have', MAX)

score = 0
for line in data:
    game_id, draws = re.fullmatch(r'Game (\d+): (.*)', line).groups()
    game_id = int(game_id)
    possible = True
    for draw in draws.split('; '):
        for colorcount in draw.split(', '):
            num, color = colorcount.split(' ')
            print(f'{game_id}: {num} {colorcount}')
            if int(num) > MAX[color]:
                print('-> impossible!')
                possible = False
                break
    if possible:
        score += game_id
    print(f'... {score=}')


print('*** part 1:', score)


score = 0
for line in data:
    fewest = {
        'red': 0,
        'green': 0,
        'blue': 0,
    }
    game_id, draws = re.fullmatch(r'Game (\d+): (.*)', line).groups()
    game_id = int(game_id)
    for draw in draws.split('; '):
        for colorcount in draw.split(', '):
            num, color = colorcount.split(' ')
            fewest[color] = max(fewest[color], int(num))
            print(f'{game_id}: {num} {colorcount}. {fewest=}')
    power = functools.reduce(operator.mul, fewest.values())
    score += power
    print(f'... {power=} {score=}')



print('*** part 2:', score)
