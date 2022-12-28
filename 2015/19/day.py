import sys
import re
import itertools
import collections
import string

data = sys.stdin.read().strip().splitlines()

molecule = data[-1]

# Give everythng a 1-letter nickname
ALIASES = {
    'Rn': '(',
    'Ar': ')',
    'Ca': '-',
    'Si': '<',
    'Th': '>',
    'Mg': '%',
    'Al': '!',
    'Ti': '#',
    'B': ':',
    'P': ';',
    'F': '^',
    'Y': '_',
    'e': '$',
}
def replace_aliases(s):
    for key, val in ALIASES.items():
        s = s.replace(key, val)
    assert not any(c in string.ascii_lowercase for c in s)
    return s

recipes = {}
for line in data[:-1]:
    if line:
        src, dst = line.split(' => ')
        src = replace_aliases(src)
        dst = replace_aliases(dst)
        recipes.setdefault(src, []).append(dst)
for src, dst in recipes.items():
    print(src, '=>', dst)


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
print(f'*** part 1: {len(result)}')

# For part 2, ignore "C" since it's not in the molecule and can't be replaced
# by anything else.

molecule = replace_aliases(molecule)
assert 'C' not in molecule
print(molecule)

rev_recipes = {}
for line in data[:-1]:
    if line:
        dst, src = line.split(' => ')
        src = replace_aliases(src)
        dst = replace_aliases(dst)
        assert dst != 'C'
        if 'C' in src:
            continue
        assert src not in rev_recipes
        rev_recipes[src] = dst
for src, dst in rev_recipes.items():
    print(f'{src:>6} => {dst}')

def gen_rev_replacements(molecule, rev_recipes, first_index=-1, last_index=-1):
    for src, dst in rev_recipes.items():
        index = first_index
        while True:
            try:
                index = molecule.index(src, index+1)
            except ValueError:
                break
            if index > last_index > 0:
                break
            prefix = molecule[:index]
            suffix = molecule[index + len(src):]
            yield prefix + dst + suffix

# In my input, Rn and Ar act as "brackets".
# We'll handle the first innermost bracket first.
# But before that, check the assumption.
for rule in rev_recipes:
    if ')' in rule:
        assert rule.count(')') == 1
        assert rule.count('(') == 1
        assert rule.endswith(')')

# Put `(x)` (one character between Rn/Ar) on a "must replace" list
must_replace = {
    src: dst for src, dst in rev_recipes.items()
    if re.search(r'\(.\)', src)
}

# A `-` should be deleted ASAP; there's nothing more useful to do with it
for src, dst in rev_recipes.items():
    if '-' in src:
        assert src in ('-' + dst, dst + '-')
        must_replace[src] = dst

# A `_` appears in nothing but bracketed stuff
for src, dst in rev_recipes.items():
    if '_' in src:
        assert '(' in src and src.index('(') < src.index('_') < src.index(')')
        must_replace[src] = dst
    must_replace['(' + src + ')'] = '(' + dst + ')'

molecules = {molecule}
seen = set()
for step_number in itertools.count():
    print(f'step {step_number}: {len(molecules)} molecules')
    print(
        f'len(min)={min(len(m) for m in molecules)}'
        + f' len(max)={max(len(m) for m in molecules)}'
        + f' len(seen)={len(seen)}'
    )
    print(f'min:{min(molecules, key=len)}')
    print(f'max:{max(molecules, key=len)}')
    print(collections.Counter(m.count(')') for m in molecules))
    if len(molecules) < 10:
        print(molecules)
    if '$' in molecules:
        print(f'*** part 2: {step_number}')
        break
    new_molecules = set()
    for molecule in molecules:
        for src, dst in must_replace.items():
            index = molecule.find(src)
            if index >= 0:
                gen = [molecule[:index] + dst + molecule[index+len(src):]]
                break
        else:
            first_ar = molecule.find(')')
            if first_ar >= 0:
                matching_rn = molecule.rfind('(', 0, first_ar)
                rn_before = molecule.rfind('(', 0, matching_rn)
                #print('--', molecule[rn_before:first_ar], rn_before, first_ar)
                gen = gen_rev_replacements(
                    molecule, rev_recipes,
                    first_index=rn_before,
                    last_index=first_ar,
                )
            else:
                gen = gen_rev_replacements(molecule, rev_recipes)
        for new in gen:
            if new not in seen:
                seen.add(new)
                new_molecules.add(new)
                if len(new_molecules) % 100_000 == 0:
                    print(
                        len(new_molecules),
                        min(len(m) for m in new_molecules),
                        max(len(m) for m in new_molecules),
                    )
    molecules = new_molecules
