import sys
from collections import Counter
from pprint import pprint

data = sys.stdin.read().strip().splitlines()

def solve(data, pos=0):
    for line in data:
        try:
            for char, counter in zip(line, counters):
                counter.update(char)
        except NameError:
            counters = tuple(Counter(char) for char in line)
    pprint(list(c.most_common(3)+c.most_common()[-3:] for c in counters))
    return ''.join(c.most_common()[pos][0] for c in counters)

example = """
eedadn
drvtee
eandsr
raavrd
atevrs
tsrnev
sdttsa
rasrtv
nssdts
ntnada
svetve
tesnvt
vntsnd
vrdear
dvrsen
enarar
""".strip().splitlines()

assert solve(example) == 'easter'
print(f'*** part 1: {solve(data)}')

assert solve(example, -1) == 'advent'
print(f'*** part 2: {solve(data, -1)}')
