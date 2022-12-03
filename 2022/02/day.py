import sys

data = sys.stdin.read().splitlines()
print(data)

# 0=rock, 1=paper, 2=scissors
# N loses to N+1 (with wrap-around, so 3=rock)
# N beats N-1 (with wrap-around, so -1=scissors)
# (wrap-around meand modulo 3)
SYMBOLS = 'RPS'

def get_outcome(my, their):
    # 0 - lose (my == their-1)
    # 3 - draw (my == their)
    # 6 - win  (my == their+1)
    return (my - their + 1) % 3 * 3

def get_score_and_log(my, their):
    outcome = get_outcome(my, their)
    print(f"{SYMBOLS[my]}/{SYMBOLS[their]} {my+1:+} {outcome:+}")
    return (my + 1) + outcome

score = 0
for row in data:
    their, my = row.split()
    my = 'XYZ'.index(my)
    their = 'ABC'.index(their)
    score += get_score_and_log(my, their)

print('*** part 1:', score)


score = 0
move_scores = {m:s for s, m in enumerate('RPS', start=1)}
for row in data:
    their, my = row.split()
    their = 'ABC'.index(their)
    my = (their + 'XYZ'.index(my) - 1) % 3
    score += get_score_and_log(my, their)


print('*** part 2:', score)
