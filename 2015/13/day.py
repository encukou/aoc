import sys
import re
import itertools

data = sys.stdin.read().strip().splitlines()

LINE_RE = re.compile(
    '(\w+) would (\w+) (\d+) happiness units by sitting next to (\w+).'
)
DIRECTIONS = {'gain': +1, 'lose': -1}

def parse_data(data):
    relationships = {}
    for line in data:
        a, direction, amount, b = LINE_RE.match(line).groups()
        relationships[a, b] = DIRECTIONS[direction] * int(amount)
    return relationships
relationships = parse_data(data)

def get_best(relationships):
    guests = sorted(set().union(*relationships))
    return max(
        sum(
            relationships[a, b] + relationships[b, a]
            for a, b in
            zip(permutation, (*permutation[1:], permutation[0]))
        )
        for permutation in itertools.permutations(guests)
    )

example = """
Alice would gain 54 happiness units by sitting next to Bob.
Alice would lose 79 happiness units by sitting next to Carol.
Alice would lose 2 happiness units by sitting next to David.
Bob would gain 83 happiness units by sitting next to Alice.
Bob would lose 7 happiness units by sitting next to Carol.
Bob would lose 63 happiness units by sitting next to David.
Carol would lose 62 happiness units by sitting next to Alice.
Carol would gain 60 happiness units by sitting next to Bob.
Carol would gain 55 happiness units by sitting next to David.
David would gain 46 happiness units by sitting next to Alice.
David would lose 7 happiness units by sitting next to Bob.
David would gain 41 happiness units by sitting next to Carol.
""".strip().splitlines()

print(get_best(parse_data(example)))

print('*** part1:', get_best(relationships))

for guest in set().union(*relationships):
    relationships['me', guest] = 0
    relationships[guest, 'me'] = 0

print('*** part2:', get_best(relationships))
