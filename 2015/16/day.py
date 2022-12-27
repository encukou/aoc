import sys
import re

data = sys.stdin.read().strip().splitlines()

def parse_evidence_line(line):
    group, n = line.strip().split(':')
    return group, int(n)

evidence = dict(
    parse_evidence_line(line)
    for line in """
        children: 3
        cats: 7
        samoyeds: 2
        pomeranians: 3
        akitas: 0
        vizslas: 0
        goldfish: 5
        trees: 3
        cars: 2
        perfumes: 1
        """.strip().splitlines()
)
for n, line in enumerate(data):
    sue = {k: int(n) for k, n in re.findall('(\w+): (\d+)', line)}
    if evidence.items() >= sue.items():
        print(line)
        print('*** part1:', line.split()[1].strip(':'))

greater = {'cats', 'trees'}
lower = {'pomeranians', 'goldfish'}

for n, line in enumerate(data):
    for item_kind, n in re.findall('(\w+): (\d+)', line):
        n = int(n)
        if item_kind in greater:
            if not (n > evidence[item_kind]):
                break
        elif item_kind in lower:
            if not (n < evidence[item_kind]):
                break
        else:
            if not (n == evidence[item_kind]):
                break
    else:
        print(line)
        print('*** part2:', line.split()[1].strip(':'))
