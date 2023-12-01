import sys
from dataclasses import dataclass

@dataclass
class Program:
    name: str
    weight: int
    children: frozenset

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

def part1(rows):
    remaining = [parse(row) for row in rows]
    structure = {}
    while remaining:
        todo = list(remaining)
        remaining = []
        for program in todo:
            print(program)
            if program.children - frozenset(structure):
                remaining.append(program)
            else:
                structure[program.name] = program
    return program.name

print('*** part 1:', part1(data))




print('*** part 2:', ...)
