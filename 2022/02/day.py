from pathlib import Path
import os
SMALLDATA = 'SMALLDATA' in os.environ

data = """
A Y
B X
C Z
""".strip()
if not SMALLDATA:
    data = Path('input.txt').read_text()
    ...

data = data.splitlines()
print(data)

def get_score(my, their):
    if my == their:
        return 3
    if my + their in {'RS', 'SP', 'PR'}:
        return 6
    return 0

cipher = dict('AR BP CS XR YP ZS'.split())

score = 0
move_scores = {m:s for s, m in enumerate('RPS', start=1)}
for row in data:
    their, my = row.split()
    my = cipher[my]
    their = cipher[their]
    score += move_scores[my]
    score += get_score(my, their)
    print(my, their, score)

print(get_score(*'SP'))

part1 = score
print('part 1:', part1)
if SMALLDATA:
    assert part1 == 15


score = 0
move_scores = {m:s for s, m in enumerate('RPS', start=1)}
for row in data:
    their, my = row.split()
    their = cipher[their]
    if my == 'X':
        my = dict({'RS', 'SP', 'PR'})[their]
    elif my == 'Y':
        my = their
    elif my == 'Z':
        my = dict({'RP', 'SR', 'PS'})[their]
    score += move_scores[my]
    score += get_score(my, their)
    print(my, their, score)



part2 = score
print('part 2:', part2)
if SMALLDATA:
    assert part2 == 12
