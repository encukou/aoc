import sys
import re
from itertools import zip_longest
from heapq import heappush, heappop
from dataclasses import dataclass, field, replace
import functools
import pprint

BLUEPRINT_RE = re.compile(r'Blueprint (\d+)')
MATERIALS = {k: n for n, k in enumerate(('geode', 'obsidian', 'clay', 'ore'))}
ORE = MATERIALS['ore']
GEODE = MATERIALS['geode']
ZEROS = tuple([0] * len(MATERIALS))

# Goal must be first
assert GEODE == 0

TURNS = 24

if sys.argv[1:]:
    with open(sys.argv[1]) as f:
        data = f.read().splitlines()
else:
    data = sys.stdin.read().splitlines()

def tuple_replace(orig, n, replacement):
    return *orig[:n], replacement, *orig[n+1:]

@functools.lru_cache
def max_materials(recipes):
    r = tuple((max(m) for m in zip(*recipes)))
    r = tuple_replace(r, GEODE, TURNS)
    print(recipes, '->', r)
    return r

@functools.lru_cache
def clamp_materials(materials, recipes):
    return (
        materials[0],
        *(min(m) for m in zip(materials[1:], max_materials(recipes)[1:]))
    )

@dataclass(frozen=True, order=True)
class Node:
    recipes: list = field(compare=False, repr=False)
    score: int = field(compare=False, default=None)
    order: list = None
    minutes_remaining: int = TURNS
    robots: tuple = tuple_replace(ZEROS, ORE, 1)
    materials: tuple = ZEROS
    prev: object = field(compare=False, default=None, repr=False)
    optimistic_estimate: int = field(compare=False, default=None)

    def __post_init__(self):
        """
        ore = self.materials[ORE]
        ore_robots = self.robots[ORE]
        geo = self.materials[GEODE]
        geo_robots = self.robots[GEODE]
        #cost = min(
            #self.recipes[ORE][ORE],
            #self.recipes[GEODE][ORE],
        #)
        for i in range(self.minutes_remaining):
            geo += geo_robots
            geo_robots += 1
        object.__setattr__(self, 'optimistic_estimate', geo)
        """
        object.__setattr__(self, 'score', self.materials[GEODE])
        object.__setattr__(
            self, 'order',
            tuple(-n for n in self.robots + self.materials),
        )

    @property
    def minute(self):
        return TURNS-self.minutes_remaining

    def __repr__(self):
        def f(t):
            return '(' + ','.join(f'{n:2}' for n in t) + ')'
        return f'<@{self.minute:2}: s={self.score} m={f(self.materials)} r={f(self.robots)} o={self.order}>'

    def is_better_than(self, other):
        return (
            all(s>=o for s, o in zip(self.materials, other.materials))
            and all(s>=o for s, o in zip(self.robots, other.robots))
        )

    def gen_next_nodes(self):
        if self.minutes_remaining <= 0:
            return
        have = self.materials
        max_mat = max_materials(self.recipes)
        built = False
        def _gather(materials, robots):
            return (
                materials[0] + robots[0],
                *tuple(
                    mm
                    if (r>=mm) else
                    mm*self.minutes_remaining
                    if (m+r > mm*self.minutes_remaining) else
                    m+r
                    for m, r, mm
                    in zip(materials, robots, max_mat)
                )[1:],
            )
        for recipe_idx, recipe in enumerate(self.recipes):
            #if recipe_idx==ORE and have == ( 0, 0, 0, 3): breakpoint()
            new_have = tuple((h - c for h, c in zip(have, recipe)))
            new_robots = self.robots
            if (
                all(n >= 0 for n in new_have)
                and self.robots[recipe_idx] < max_mat[recipe_idx]
            ):
                # Build a robot!
                built = True
                new_robots = tuple_replace(
                    new_robots, recipe_idx, new_robots[recipe_idx] + 1
                )
                new_have = _gather(new_have, self.robots)
                new_robots = clamp_materials(
                    new_robots,
                    self.recipes,
                )
                yield replace(
                    self,
                    minutes_remaining=self.minutes_remaining - 1,
                    robots=new_robots,
                    materials=new_have,
                    prev=self,
                )
        yield replace(
            self,
            minutes_remaining=self.minutes_remaining - 1,
            materials=_gather(self.materials, self.robots),
            prev=self,
        )

def get_quality_level(line):
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

    best_by_minute = {}

    visited = set()
    to_visit = [Node(recipes)]
    best_score = -1
    n = 0
    while to_visit:
        node = heappop(to_visit)
        if node in visited:
            continue
        visited.add(node)
        #if node.optimistic_estimate < best_score:
            #continue

        if node.minute == 3 and node.robots==(0,0,1,1):
            print('!', node)
        if node.minute == 4 and node.robots==(0,0,1,1):
            print('!', node)
        if node.minute == 5 and node.robots==(0,0,2,1):
            print('!', node)
        if node.minute == 6 and node.robots==(0,0,2,1):
            print('!', node)
        if node.minute == 7 and node.robots==(0,0,3,1):
            print('!', node)
        if node.minute == 8 and node.robots==(0,0,3,1):
            print('!', node)
        if node.minute == 9 and node.robots==(0,0,3,1):
            print('!', node)
        #if node.minute == 10 and node.robots==(0,0,3,1):
            #print('!', node)

        bad = False
        bbm = best_by_minute.setdefault(node.minutes_remaining, set())
        if node.minutes_remaining == 21:
            print(f'{node=}')
            print(f'{bbm=}')
            #breakpoint()
        for other in list(bbm):
            if other.is_better_than(node):
                bad = True
                break
            if node.is_better_than(other):
                bbm.remove(other)
        if bad:
            # All other nodes are better than this one
            continue
        else:
            bbm.add(node)

        n += 1
        if n % 1000 == 0:
            print('p', node, flush=True)
            #print(dict(sorted((mr, len(s)) for mr, s in best_by_minute.items())))
            #pprint.pprint(best_by_minute)

        if node.score > best_score:
            best_score = node.score
            best = node
            print(f'new best {best_score}')
            h = best
            while h is not None:
                print(h)
                h = h.prev
            print(flush=True)
        for new_node in node.gen_next_nodes():
            #if node.optimistic_estimate > best_score:
                heappush(to_visit, new_node)

    print(f'{best}')

    print(recipes)
    print(f'{best_score=}, {blueprint_number=}')
    return best_score * blueprint_number

answer = 0
for line in data:
    answer += get_quality_level(line)

print('*** part 1:', answer)




print('*** part 2:', ...)
