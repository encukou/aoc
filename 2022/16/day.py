import sys
import re
from dataclasses import dataclass, field
from pprint import pprint
from heapq import heappush, heappop

data = sys.stdin.read().splitlines()

@dataclass
class Room:
    name: str
    rate: int
    connections: list

LINE_RE = re.compile(
    r'Valve (\w+) has flow rate=(\d+); tunnels? leads? to valves? (.+)'
)

rooms = {}
for line in data:
    name, rate, connections = LINE_RE.match(line).groups()
    rooms[name] = Room(name, int(rate), connections.split(', '))
pprint(rooms)

max_rate = sum(r.rate for r in rooms.values())

@dataclass(unsafe_hash=True)
class Node:
    flowed: int
    rate: int
    minute: int
    current: str
    to_open: frozenset
    history: tuple = field(default=(), repr=False, hash=False)

    def __post_init__(self):
        self.heuristic = self.flowed + (30-self.minute) * max_rate

    def __lt__(self, other):
        return self.heuristic > other.heuristic

visited = set()
to_visit = [
    Node(0, 0, 1, 'AA', frozenset(r for r in rooms if rooms[r].rate))
]
best = None
n = 0
while to_visit:
    node = heappop(to_visit)
    if node.minute == 30:
        if best is None or node.heuristic > best.heuristic:
            best = node
        continue
    if best and node.heuristic < best.heuristic:
        continue
    visited.add(node)
    n += 1
    if n % 1000 == 0:
        print(node, flush=True)
    if node.current in node.to_open:
        new_rate = node.rate + rooms[node.current].rate
        heappush(to_visit, Node(
            node.flowed + new_rate,
            new_rate,
            node.minute + 1,
            node.current,
            node.to_open - {node.current},
            node.history + (node,),
        ))
    for conn in rooms[node.current].connections:
        heappush(to_visit, Node(
            node.flowed + node.rate,
            node.rate,
            node.minute + 1,
            conn,
            node.to_open,
            node.history + (node,),
        ))
print()
for n in best.history:
    print(n)
print(best)

print('*** part 1:', best.flowed)




print('*** part 2:', ...)
