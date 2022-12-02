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

data = data.splitlines()
print(data)

SYMBOLS = 'RPS'

def get_outcome(my, their):
    return (my - their + 1) % 3 * 3

def get_score_and_log(my, their):
    outcome = get_outcome(my, their)
    print(f"{SYMBOLS[my]}/{SYMBOLS[their]} {my+1:+} {outcome:+}")
    return my + 1 + outcome

score = 0
for row in data:
    their, my = row.split()
    my = 'XYZ'.index(my)
    their = 'ABC'.index(their)
    score += get_score_and_log(my, their)

part1 = score
print('part 1:', part1)
if SMALLDATA:
    assert part1 == 15


score = 0
move_scores = {m:s for s, m in enumerate('RPS', start=1)}
for row in data:
    their, my = row.split()
    their = 'ABC'.index(their)
    my = (their + 'XYZ'.index(my) - 1) % 3
    score += get_score_and_log(my, their)


part2 = score
print('part 2:', part2)
if SMALLDATA:
    assert part2 == 12
