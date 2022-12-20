import sys
import re
from dataclasses import dataclass, field, replace
from pprint import pprint
from functools import partial, lru_cache

pprint = partial(pprint, width=50)

if sys.argv[1:]:
    with open(sys.argv[1]) as f:
        data = f.read().splitlines()
else:
    data = sys.stdin.read().splitlines()

LINE_RE = re.compile(r'Blueprint (\d+): Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian.')

print(data)

@dataclass
class Blueprint:
    number: int
    costs: tuple
    max_costs: tuple

blueprints = []
for line in data:
    blueprint_number, ore_cost, clay_cost, obs_cost_ore, obs_cost_clay, geo_cost_ore, geo_cost_obs = (int(n) for n in LINE_RE.match(line).groups())
    print(*(int(n) for n in LINE_RE.match(line).groups()))
    costs=(
        (ore_cost, 0, 0, 0),
        (clay_cost, 0, 0, 0),
        (obs_cost_ore, obs_cost_clay, 0, 0),
        (geo_cost_ore, 0, geo_cost_obs, 0),
    )
    blueprint = Blueprint(
        number=blueprint_number,
        costs=costs,
        max_costs=(
            *[max(c) for c in zip(*costs)][:-1],
            float('inf'),
        ),
    )
    blueprints.append(blueprint)
pprint(blueprints)

@dataclass(frozen=True)
class Node:
    minutes_remaining: int
    blueprint: Blueprint = field(repr=False, compare=False)
    materials: tuple = (0, 0, 0, 0)
    robots: tuple = (1, 0, 0, 0)

    @property
    def score(self):
        return self.materials[-1]

    @property
    @lru_cache
    def optimistic_estimate(self):
        # A number that's bigger (or same) as the best
        # score achievable from this node.
        mr = self.minutes_remaining
        return (
            self.score
            + self.robots[-1] * mr
            + (mr+1) * mr // 2
        )

    def __repr__(self):
        def f(resources):
            return '(' + ','.join(f'{n:2}' for n in resources) + ')'
        return f'<{self.minutes_remaining:2}: m={f(self.materials)} r={f(self.robots)}>'

    def generate_next_nodes(self):
        # Buy robots of all kinds if able
        built_a_robot = False
        for robot_i, (
            cost, current_robot_count, max_cost
        ) in enumerate(zip(
            self.blueprint.costs,
            self.robots,
            self.blueprint.max_costs,
        )):
            # Don't buy robots we're not getting resources
            # for
            if any(
                c > 0 and r == 0
                for c, r in zip(cost, self.robots)
            ):
                continue
            if current_robot_count >= max_cost:
                continue
            materials = self.materials
            minutes_remaining = self.minutes_remaining
            while minutes_remaining:
                # Can we afford this robot yet?
                if all(
                    m >= c
                    for m, c in zip(materials, cost)
                ):
                    # Yes!
                    break
                # Spend this turn gathering resources
                minutes_remaining -= 1
                materials = tuple(
                    m + r
                    for m, r in zip(materials, self.robots)
                )
            if minutes_remaining:
                # Spend resources for robot
                materials = tuple(
                    m - c
                    for m, c in zip(materials, cost)
                )
                minutes_remaining -= 1
                # Robots gather resources
                materials = tuple(
                    m + r
                    for m, r in zip(materials, self.robots)
                )
                robots = tuple(
                    r + (1 if robot_i == i else 0)
                    for i, r in enumerate(self.robots)
                )
                yield replace(
                    self,
                    minutes_remaining=minutes_remaining,
                    materials=tuple(
                        min(
                            m,
                            mc + (mc-r)*minutes_remaining
                        )
                        for m, mc, r in zip(
                            materials,
                            self.blueprint.max_costs,
                            robots,
                        )
                    ),
                    robots=robots,
                )
                built_a_robot = True

        if not built_a_robot and self.minutes_remaining:
            # Wait
            materials = tuple(
                m + r * self.minutes_remaining
                for m, r in zip(self.materials, self.robots)
            )
            yield replace(
                self,
                minutes_remaining=0,
                materials=materials,
            )

def get_best_score(blueprint, total_minutes):
    to_visit = [Node(
        minutes_remaining=total_minutes,
        blueprint=blueprint,
    )]
    best_score = -1
    best_node = None
    n = 0
    visited = set()
    while to_visit:
        node = to_visit.pop()
        if node.optimistic_estimate < best_score:
            continue
        if node in visited:
            continue
        visited.add(node)
        n += 1
        if n % 10_000 == 0:
            print(n, node)
        if node.score > best_score:
            print(f'best {blueprint.number}:', node)
            best_score = node.score
            best_node = node
        for new_node in node.generate_next_nodes():
            to_visit.append(new_node)
    return best_node.score

answer = 0
for blueprint in blueprints:
    geodes = get_best_score(blueprint, 24)
    print(f'{blueprint.number=}: {geodes=}')
    answer += geodes * blueprint.number

print(f'part 1 {answer=}')

answer = 1
for blueprint in blueprints[:3]:
    geodes = get_best_score(blueprint, 32)
    print(f'{blueprint.number=}: {geodes=}')
    answer *= geodes

print(f'part 2 {answer=}')
