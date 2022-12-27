import sys
import re
import itertools
import functools
import operator

data = sys.stdin.read().strip().splitlines()

LINE_RE = re.compile(
    '\w+: capacity (-?\d+), durability (-?\d+), flavor (-?\d+), texture (-?\d+), calories (-?\d+)'
)

ingredients = []
for line in data:
    ingredients.append(tuple(int(n) for n in LINE_RE.match(line).groups()))

best = 0
best_500 = 0
for amounts in itertools.product(range(100), repeat=len(ingredients)-1):
    rest = 100 - sum(amounts)
    if rest < 0:
        continue
    amounts = (*amounts, rest)
    properties = [sum(p) for p in zip(*(
        tuple(prop * amount for prop in ingredient)
        for ingredient, amount in zip(ingredients, amounts)
    ))]
    if any(p < 0 for p in properties):
        continue
    else:
        result = functools.reduce(operator.mul, properties[:-1])
        if result > best:
            best = result
            print(amounts, result, properties)
        if properties[-1] == 500 and result > best_500:
            best_500 = result
            print(amounts, result, properties)

print('*** part1:', best)
print('*** part2:', best_500)
