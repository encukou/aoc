import sys
import re
import itertools

ATOM_RE = re.compile('[A-Z][a-z]*')

data = sys.stdin.read().strip().splitlines()

recipes = {}
rev_recipes = {}
for line in data[:-1]:
    if line:
        src, dst = line.split(' => ')
        recipes.setdefault(src, []).append(dst)
        rev_recipes.setdefault(dst, []).append(src)
print(recipes)

molecule = data[-1]
print(molecule)

def gen_replacements(molecule, recipes):
    for src in recipes:
        index = -1
        while True:
            try:
                index = molecule.index(src, index+1)
            except ValueError:
                break
            prefix = molecule[:index]
            suffix = molecule[index + len(src):]
            for replacement in recipes[src]:
                yield prefix + replacement + suffix

result = set()
for n, r in enumerate(gen_replacements(molecule, recipes)):
    result.add(r)
if len(result) < 10:
    print(result)
print(f'*** part 1: {len(result)}')
