import sys
import re

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




print('*** part 2:', ...)
