import sys
import re
from dataclasses import dataclass, field, replace
from pprint import pprint
from heapq import heappush, heappop
from functools import partial

if sys.argv[1:]:
    with open(sys.argv[1]) as f:
        data = f.read().splitlines()
else:
    data = sys.stdin.read().splitlines()

@dataclass
class Room:
    name: str
    rate: int
    connections: list

    replace = replace

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

# Add conections to all rooms
for name, room in rooms.items():
    if room.rate or room.name =='AA':
        to_visit = list(room.connections.items())
        all_connections = {}
        while to_visit:
            next_name, dist = to_visit.pop()
            now = all_connections.get(next_name)
            if now is None or now > dist:
                all_connections[next_name] = dist
                for far_name, dist2 in rooms[next_name].connections.items():
                    if far_name != name:
                        to_visit.append((far_name, dist+dist2))
        if set(all_connections) != set(rooms) - {name}:
            print(name)
            print(sorted(set(all_connections)))
            print(sorted(set(rooms) - {name}))
            raise AssertionError('^')
        room.connections = {
            r: d for r, d in all_connections.items()
        }

# Remove useless rooms
rooms = {
    room.name: room.replace(
        connections={r: d for r, d in room.connections.items() if rooms[r].rate}
    )
    for room in rooms.values()
    if room.rate or room.name =='AA'
}

pprint(rooms)

MAX_RATE = sum((r.rate for r in rooms.values()))

@dataclass(frozen=True, order=True)
class Actor:
    steps_remaining: int
    action: str
    room_name: str

    replace = replace

    def __str__(self):
        if self.steps_remaining:
            cc = f'{self.steps_remaining}'
        else:
            cc = ' '
        if self.action == 'goto':
            return f'{cc}{self.room_name.lower()}'
        return f'{cc}{self.room_name}'

@dataclass(frozen=True, order=True)
class Node:
    optimistic_estimate: int
    score: int = field(compare=False)
    flowed: int = field(compare=False)
    rate: int = field(compare=False)
    min_remaining: int
    to_open: frozenset
    opened: frozenset
    actors: tuple
    history: tuple = field(compare=False)
    min_total: int = field(compare=False)

    def __repr__(self):
        return f'<{self.min_total-self.min_remaining:02}:{self.flowed:4}+{self.rate:3}/m {self.score:4}-{self.optimistic_estimate:4} a=[{",".join(str(a) for a in self.actors)}] {"".join(str(n.actors[0]) for n in self.history)}>'

    def replace(self, flowed=None, min_remaining=None, rate=None, **kwargs):
        flowed = flowed or self.flowed
        if min_remaining is None:
            min_remaining = self.min_remaining
        rate = rate or self.rate

        score = flowed + rate * min_remaining

        optimistic_estimate = flowed
        optimistic_rate = rate
        rates_to_open = sorted(
            (rooms[r].rate for r in self.to_open | self.opened),
        )
        for i in range(min_remaining):
            if rates_to_open:
                optimistic_rate += rates_to_open.pop()
            optimistic_estimate += optimistic_rate
        #optimistic_estimate = flowed + MAX_RATE * min_remaining

        return replace(
            self,
            **kwargs,
            flowed=flowed,
            rate=rate,
            min_remaining=min_remaining,
            optimistic_estimate=optimistic_estimate,
            score=score,
        )

    def gen_next_nodes(self, actor_index=0):
        if actor_index == len(self.actors):
            # Do scheduled work.
            steps = min(a.steps_remaining for a in self.actors)
            if not self.min_remaining:
                return
            if steps >= self.min_remaining:
                steps = self.min_remaining
            if not steps:
                return
            new_flowed = self.flowed + self.rate * steps
            new_node = self.replace(
                flowed=new_flowed,
                min_remaining=self.min_remaining - steps,
                history=list(self.history),
                actors=tuple((
                    a.replace(steps_remaining=a.steps_remaining - steps)
                    for a in self.actors
                )),
            )
            new_node.history.append(new_node)
            yield new_node
            return
        actor = self.actors[actor_index]
        if actor.steps_remaining:
            yield from self.gen_next_nodes(actor_index + 1)
        elif actor.action == 'goto':
            if actor.room_name in self.to_open:
                # Start opening valve
                yield from self.replace(
                    actors=tuple_replace(
                        self.actors, actor_index,
                        Actor(1, 'open', actor.room_name),
                    ),
                    to_open=self.to_open - {actor.room_name},
                ).gen_next_nodes(actor_index + 1)
        elif actor.action == 'open':
            # Finish opening valve
            new_rate = self.rate + rooms[actor.room_name].rate
            done = self.replace(
                rate=new_rate,
                opened=self.opened | {actor.room_name},
            )
            # Embark on new journeys
            embarked = False
            for conn, dist in rooms[actor.room_name].connections.items():
                if conn in self.to_open:
                    embarked = True
                    yield from done.replace(
                        actors=tuple_replace(
                            self.actors, actor_index,
                            Actor(dist, 'goto', conn),
                        ),
                    ).gen_next_nodes(actor_index + 1)
            # Or wait here
            yield from done.replace(
                actors=tuple_replace(
                    self.actors, actor_index,
                    Actor(self.min_remaining, 'goto', actor.room_name),
                ),
            ).gen_next_nodes(actor_index + 1)
        else:
            raise ValueError(actor.action)

def tuple_replace(orig, n, replacement):
    return *orig[:n], replacement, *orig[n+1:]

def solve(num_actors, min_remaining, best_score=0):
    max_rate = sum((r.rate for r in rooms.values()))
    print('max_rate=', max_rate)

    visited = set()
    to_visit = [Node(
        flowed=0,
        rate=0,
        min_remaining=min_remaining,
        to_open=frozenset(r for r in rooms if rooms[r].rate),
        opened=frozenset(),
        score=0,
        optimistic_estimate=min_remaining * max_rate,
        actors=(Actor(0, 'open', 'AA'), ) * num_actors,
        history=[],
        min_total=min_remaining,
    )]
    to_visit[0].history.append(replace(to_visit[0], history=()))
    best = None
    n = 0
    while to_visit:
        node = heappop(to_visit)

        log_details = False

        if node in visited:
            if log_details:
                print('v', new_node)
            continue
        visited.add(replace(node, history=None))
        if node.optimistic_estimate < best_score:
            if log_details:
                print('x', new_node)
            continue
        if log_details:
            print('p', new_node)

        n += 1
        if n % 10_000 == 0 or n < 100 or not node.flowed:
            print(node, len(visited), '<-', len(to_visit), 'b', best_score, flush=True)

        if node.score > best_score:
            best_score = node.score
            best = node
            print(best, flush=True)
        for new_node in node.gen_next_nodes():
            if log_details:
                print('.', new_node)
            if node.optimistic_estimate > best_score:
                heappush(to_visit, new_node)
                if log_details:
                    print('+', new_node)

    print()
    for node in best.history:
        print(node)
    return best.score

part1 = solve(1, 30)
print('*** part 1:', part1)

print('*** part 2:', solve(2, 26))
