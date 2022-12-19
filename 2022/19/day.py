import sys
import re
from itertools import zip_longest
from dataclasses import dataclass, field, replace
from functools import cached_property

BLUEPRINT_RE = re.compile(r'Blueprint (\d+)')
MATERIALS = {k: n for n, k in enumerate(('geode', 'obsidian', 'clay', 'ore'))}
ORE = MATERIALS['ore']
GEODE = MATERIALS['geode']
ZEROS = tuple([0] * len(MATERIALS))
INITIAL_ROBOTS = (*ZEROS[:-1], 1)

# Goal must be first, inintial robot last
assert GEODE == 0

if sys.argv[1:]:
    with open(sys.argv[1]) as f:
        data = f.read().splitlines()
else:
    data = sys.stdin.read().splitlines()

def parse_blueprint(line):
    blueprint_header, recipes_text = line.split(':')
    blueprint_number = int(BLUEPRINT_RE.match(blueprint_header)[1])
    recipes = [0] * len(MATERIALS)
    for recipe_text in recipes_text.split('.'):
        words = recipe_text.split()
        if not words:
            continue
        assert words[0] == 'Each'
        robot_type = words[1]
        assert words[2] == 'robot'
        assert words[3] == 'costs'
        material_text = words[4:]
        materials = [0] * len(MATERIALS)
        for num, mat, _and in zip_longest(material_text[::3], material_text[1::3], material_text[2::3]):
            materials[MATERIALS[mat]] += int(num)
            assert _and in (None, "and")
        recipes[MATERIALS[robot_type]] = tuple(materials)
    recipes = tuple(recipes)
    return blueprint_number, recipes
blueprints = tuple(parse_blueprint(line) for line in data)
print(blueprints)

@dataclass
class Problem:
    recipes: tuple
    total_minutes: int

    @cached_property
    def max_materials(self):
        r = tuple((max(m) for m in zip(*self.recipes)))
        r = (float('inf'), *r[1:])
        return r


@dataclass
class Node:
    problem: Problem
    min_remaining: int
    materials: tuple = ZEROS
    robots: tuple = INITIAL_ROBOTS
    prev: "Node" = None
    history_entry: str = None

    def __repr__(self):
        def f(t):
            return '(' + ','.join(f'{n:2}' for n in t) + ')'
        return f'<@{self.minute:2}: m={f(self.materials)} r={f(self.robots)} {self.history}>'

    @property
    def minute(self):
        return self.problem.total_minutes - self.min_remaining

    @property
    def score(self):
        return self.materials[0]

    @property
    def history(self):
        if self.history_entry:
            return self.prev.history + self.history_entry
        return ''

    def gen_next_nodes(self):
        min_remaining = self.min_remaining
        if min_remaining == 0:
            return
        # Determine what robots we'll try to build.
        # Can't build any that need resources we don't collect yet.
        robots_remaining = {
            n: r
            for n, r in enumerate(self.problem.recipes)
            if all(rob or not rec for rec, rob in zip(r, self.robots))
        }
        materials = self.materials
        while min_remaining > 0 and robots_remaining:
            min_remaining -= 1
            for robot_idx, recipe in list(robots_remaining.items()):
                if robot_idx not in robots_remaining:
                    continue
                if self.robots[robot_idx] >= self.problem.max_materials[robot_idx]:
                    # We don't need this robot any more
                    del robots_remaining[robot_idx]
                    continue
                # Can we build it?
                if all(
                    mat >= cost
                    for mat, cost in zip(materials, recipe)
                ):
                    # Yes we can!
                    del robots_remaining[robot_idx]
                    yield replace(
                        self,
                        materials=tuple(
                            mat - cost + income
                            for mat, cost, income
                            in zip(materials, recipe, self.robots)
                        ),
                        robots=tuple(
                            r+(robot_idx==idx)
                            for idx, r in enumerate(self.robots)
                        ),
                        min_remaining=min_remaining,
                        prev=self,
                        history_entry=str(robot_idx)
                            + '⁰¹²³⁴'[len(robots_remaining)],
                    )
            # Gather materials
            materials = tuple(
                mat + income
                for mat, income
                in zip(materials, self.robots)
            )
        # If we ran out of time, yield the final state
        if not min_remaining:
            yield replace(
                self,
                materials=materials,
                min_remaining=min_remaining,
                prev=self,
                history_entry='.',
            )


def solve_blueprint(blueprint, total_minutes):
    blueprint_number, recipes = blueprint
    to_visit = [Node(
        problem=Problem(recipes, total_minutes),
        min_remaining=total_minutes,
    )]
    best = None
    best_score = -1
    n = 0
    while to_visit:
        node = to_visit.pop()

        # Progress display
        n += 1
        if n % 100_000 == 0:
            print(
                f'\x1b[K ... {n:8} {len(to_visit):3} {node.history}',
                end='\r', flush=True, file=sys.stderr,
            )

        # New best score + display
        if node.score > best_score:
            best_score = node.score
            best = node
            print(f'\x1b[K(b{blueprint_number}@{total_minutes}m) new best {best_score}!')
            h = best
            while h is not None:
                print(h)
                h = h.prev
            print(f'max_materials={node.problem.max_materials}')
            print(flush=True)

        # Generate next nodes
        for child in node.gen_next_nodes():
            to_visit.append(child)
    return best_score


answer1 = 0
for blueprint in blueprints:
    blueprint_number, recipes = blueprint
    geodes = solve_blueprint(blueprint, 24)
    answer1 += geodes * blueprint_number
    print(f'{geodes=} {blueprint_number=} {answer1=}')

print('*** part 1:', answer1)
# TEST 33 (9*1+12*2)
# REAL 1356

answer2 = 1
for blueprint in blueprints[:3]:
    geodes = solve_blueprint(blueprint, 32)
    answer2 *= geodes

print('*** part 2:', answer2)
# TEST 3472 (56*62)
# REAL:
# 25200 too low
# 1356 too low (duh)
# 27720

# 72*72*10 = 25200
# 35*72
