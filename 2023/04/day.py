import sys
import collections

data = sys.stdin.read().splitlines()
print(data)

def gen_data():
    for line in data:
        print(line)
        head, numbers = line.split(':')
        game_no = int(head.split()[-1])
        winning, have = numbers.split('|')
        winning = set(int(n) for n in winning.split())
        have = set(int(n) for n in have.split())
        yield game_no, winning, have

total = 0
for game_no, winning, have in gen_data():
    num_matches = len(winning & have)
    if num_matches:
        points = 1 << (num_matches - 1)
        total += points

print('*** part 1:', total)

copies = collections.defaultdict(int)
for game_no, winning, have in gen_data():
    copies[game_no] += 1
    num_matches = len(winning & have)
    for i in range(num_matches):
        copies[i+game_no+1] += copies[game_no]
    print(copies)


print('*** part 2:', sum(copies.values()))
