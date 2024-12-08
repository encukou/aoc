import re
import sys

data = sys.stdin.read().splitlines()
print(data)

problems = []
for line in data:
    match = re.match(r'(\d+) players; last marble is worth (\d+) points', line)
    n_players = int(match[1])
    end = int(match[2]) + 1
    problems.append((n_players, end))

if len(problems) == 1:
    n_players, end = problems[0]
    problems.append((n_players, end * 100))

results = []
for n_players, end in problems:
    circle = [0]
    current = 0
    scores = [0 for i in range(n_players)]
    for current_marble in range(1, end):
        elf = current_marble % n_players
        if current_marble < 25:
            print(elf, current, circle)
        elif current_marble % 1000 == 0:
            print(f'{current_marble}/{end}', elf, current, len(circle), flush=True)
        if current_marble % 23 == 0:
            scores[elf] += current_marble
            current -= 7
            current %= len(circle)
            scores[elf] += circle.pop(current)
        else:
            current += 2
            current %= len(circle)
            circle.insert(current, current_marble)
    results.append(max(scores))


print('*** part 1:', ' '.join(str(n) for n in results))

