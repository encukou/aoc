import sys
from dataclasses import dataclass, field, replace
from collections import deque
from itertools import chain, combinations
import re

data = sys.stdin.read().strip().splitlines()

CHIP_RE = re.compile(r' (\w+)-compatible microchip')
GEN_RE = re.compile(r' (\w+) generator')

example = """
The first floor contains a hydrogen-compatible microchip and a lithium-compatible microchip.
The second floor contains a hydrogen generator.
The third floor contains a lithium generator.
The fourth floor contains nothing relevant.
""".strip().splitlines()

@dataclass(frozen=True)
class State:
    items_by_level: tuple
    level: int
    turn_number: int = field(compare=False)
    prev: 'State' = field(compare=False)

    def __repr__(self):
        return f'<{self.turn_number}: | {" | ".join(str(lv) + ("* " if lv == self.level else ". ") + ",".join(sorted(lvitems)) for lv, lvitems in enumerate(self.items_by_level))} |>'

    def is_valid(self):
        if self.level < 0 or self.level >= len(self.items_by_level):
            return False
        for items in self.items_by_level:
            for item in items:
                if (
                    not item.endswith('G')
                    and item + 'G' not in items
                    and any(generator.endswith('G') for generator in items)
                ):
                    return False
        return True

    def is_goal(self):
        for items in self.items_by_level[:-1]:
            if items:
                return False
        return True

    def gen_next_states(self):
        can_take = self.items_by_level[self.level]
        for items_to_take in chain(combinations(can_take, 1), combinations(can_take, 2)):
            items_to_take = set(items_to_take)
            for new_level in self.level + 1, self.level - 1:
                next_state = replace(
                    self,
                    items_by_level=tuple(
                        items - items_to_take
                        if lv == self.level else
                        items | items_to_take
                        if lv == new_level else
                        items
                        for lv, items in enumerate(self.items_by_level)
                    ),
                    level=new_level,
                    turn_number=self.turn_number + 1,
                    prev=self,
                )
                if next_state.is_valid():
                    yield next_state

def solve(lines):
    items = []
    for n, line in enumerate(lines, start=1):
        items.append(frozenset({
            *(e[:2] for e in CHIP_RE.findall(line)),
            *(e[:2] + 'G' for e in GEN_RE.findall(line))
        }))
    to_visit = deque([State(
        items_by_level=tuple(items),
        level=0,
        turn_number=0,
        prev=None,
    )])
    seen = set()
    while to_visit:
        state = to_visit.popleft()
        if state in seen:
            continue
        seen.add(state)
        if len(seen) < 10 or len(seen) % 10_000 == 0:
            print(state, len(seen))
        if state.is_goal():
            return state.turn_number
        for s in state.gen_next_states():
            to_visit.append(s)

assert solve(example) == 11

print(f'*** part 1: {solve(data)}')

data[0] += """And also:
    An elerium generator.
    An elerium-compatible microchip.
    A dilithium generator.
    A dilithium-compatible microchip.
"""

# This would be better with A*...
# But memory doesn't grow all exponentially, and I need to step away
# from the computer, so... it'll run for a while.
print(f'*** part 2: {solve(data)}')
