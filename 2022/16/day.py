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
    rooms[name] = Room(
        name, int(rate), {c: 1 for c in connections.split(', ')}
    )

pprint(rooms)
print()

def gen_connections(room, visited=frozenset()):
    visited |= {room.name}
    for conn, dist in room.connections.items():
        if conn in visited:
            continue
        if rooms[conn].rate == 0:
            yield from gen_connections(rooms[conn], visited)
        else:
            yield conn, dist + len(visited) - 1

for room in rooms.values():
    room.connections = dict(sorted(
        gen_connections(room),
        key=lambda r_d: -r_d[1],
    ))
rooms = {
    room.name: room for room in rooms.values()
    if room.rate or room.name =='AA'
}

pprint(rooms)
max_rate = sum(r.rate for r in rooms.values())
print('max_rate=', max_rate)

@dataclass(unsafe_hash=True)
class Node:
    flowed: int
    rate: int
    minute: int
    heuristic: int = field(default=None, init=False)
    current: str
    to_open: frozenset
    history: tuple = field(default=(), repr=False, hash=False, compare=False)

    def __post_init__(self):
        self.heuristic = self.flowed + (40-self.minute) * max_rate

    def __lt__(self, other):
        return self.heuristic > other.heuristic

visited = set()
to_visit = [
    Node(0, 0, 1, 'AA', frozenset(rooms))
]
best = None
n = 0
while to_visit:
    node = heappop(to_visit)
    if node in visited:
        continue
    visited.add(node)
    if node.minute > 30:
        overshoot = node.minute - 30
        heappush(to_visit, Node(
            node.flowed - node.rate * overshoot,
            new_rate,
            node.minute - overshoot,
            node.current,
            node.to_open,
            node.history,
        ))
        continue
    if node.minute == 30:
        if best is None or node.flowed > best.flowed:
            best = node
        continue
    if best and node.heuristic < best.heuristic:
        continue
    n += 1
    if n % 10000 == 0:
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
    for conn, dist in rooms[node.current].connections.items():
        heappush(to_visit, Node(
            node.flowed + node.rate * dist,
            node.rate,
            node.minute + dist,
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
