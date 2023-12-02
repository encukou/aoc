import sys
import re
import operator
import math

data = sys.stdin.read().splitlines()
print(data)

def gen_data():
    for line in data:
        game_id, draws = re.fullmatch(r'Game (\d+): (.*)', line).groups()
        def parse_count_and_color(count, color):
            return int(count), color
        draws = [
            [
                parse_count_and_color(*count_and_color.split(' '))
                for count_and_color in draw.split(', ')
            ]
            for draw in draws.split('; ')
        ]
        yield int(game_id), draws

MAX = {
    'red': 12,
    'green': 13,
    'blue': 14,
}
print(f'{MAX=}')

score = 0
for game_id, draws in gen_data():
    possible = True
    for draw in draws:
        for count, color in draw:
            print(f'{game_id}: {count} {color}')
            if count > MAX[color]:
                print('-> impossible!')
                possible = False
                break
    if possible:
        score += game_id
    print(f'... {game_id=} {score=}')

print('*** part 1:', score)


score = 0
for game_id, draws in gen_data():
    fewest = {}
    for draw in draws:
        for count, color in draw:
            fewest[color] = max(fewest.get(color, 0), count)
            print(f'{game_id}: {count} {color}. {fewest=}')
    power = math.prod(fewest.values())
    score += power
    print(f'... {game_id=} {power=} {score=}')

print('*** part 2:', score)
