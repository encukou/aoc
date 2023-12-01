import sys
from dataclasses import dataclass
from pprint import pprint
from statistics import median

@dataclass
class Program:
    name: str
    weight: int
    child_names: frozenset
    children: list = None
    fullweight: int = None
    balanced: bool = None

data = sys.stdin.read().splitlines()
print(data)

def parse(row):
    print(row)
    this, sep, other = row.partition('->')
    name, weight = this.strip(') ').split(' (')
    print([this, name, weight])
    return Program(
        name.strip(),
        int(weight.strip()),
        frozenset(o.strip() for o in other.strip().split(',') if o),
    )

def build_tower(rows):
    remaining = [parse(row) for row in rows]
    structure = {}
    while remaining:
        todo = list(remaining)
        remaining = []
        for program in todo:
            print(program)
            try:
                children = [structure[c] for c in program.child_names]
            except KeyError:
                remaining.append(program)
                continue
            program.fullweight = program.weight + sum(
                c.fullweight for c in children
            )
            program.balanced = all(
                c.fullweight == children[0].fullweight
                for c in children
            )
            program.children = [c for c in children]
            if program.balanced:
                # Optimization: trim the balanced parts of tree
                program.children = []
            structure[program.name] = program
    return structure, program

structure, root = build_tower(data)

def draw(structure, root, indent=0):
    print(
        '    ' * indent,
        f'{root.name}: {root.weight} ({root.fullweight}) {"✘✓"[root.balanced]}',
    )
    for child in root.children:
        draw(structure, child, indent+1)

draw(structure, root)

print('*** part 1:', root.name)


def part2(structure, root, adjustment=None):
    weights = {c.fullweight for c in root.children}
    mid = median(c.fullweight for c in root.children)
    print(root.name, weights)
    for child in root.children:
        print(child.name)
        if not child.balanced:
            return part2(structure, child)
        if len(root.children) > 2 and child.fullweight != mid:
            [weight] = weights - {child.fullweight}
            return child.weight + (weight - child.fullweight)
        print(child.name)


print('*** part 2:', part2(structure, root))
