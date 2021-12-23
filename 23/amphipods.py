import dataclasses
import itertools
import heapq

import numpy

with open('data.txt') as f:
    lines = [line.rstrip() for line in f]

for i, line in enumerate(lines):
    lines[i] = line.ljust(len(lines[0]))

@dataclasses.dataclass
class Tile:
    connections: list[tuple[int, int]]
    can_stop: bool
    goal_for: str|None

neighbor_coords = [(0,1), (0,-1), (1,0), (-1,0)]
energy_costs = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}

goal_cols = {}
goal_rows = set()

tiles = {}
amphipods = {}
for r, line in enumerate(lines):
    goals = iter('ABCD')
    for c, char in enumerate(line):
        if char in ' #':
            continue
        connections = []
        for dr, dc in neighbor_coords:
            if lines[r + dr][c + dc] != '#':
                connections.append((r + dr, c + dc))
        if char == '.':
            goal_for = None
            can_stop = all(line[c] in ' .#' for line in lines)
        else:
            goal_for = next(goals)
            goal_cols[goal_for] = c
            goal_rows.add(r)
            can_stop = True
            amphipods[r, c] = char
        tiles[r, c] = Tile(
            connections,
            can_stop,
            goal_for,
        )

goal_rows = sorted(goal_rows)

def cheap_score(amphipods):
    score = 0
    for (r, c), a in amphipods.items():
        steps_needed = 0
        if c == goal_cols[a]:
            if r == goal_rows[-1]:
                # Already in place
                continue
            elif r == goal_rows[0]:
                apmhipod_in_bottom_goal = amphipods.get((goal_rows[-1], c))
                if apmhipod_in_bottom_goal == a:
                    # Both already in place
                    continue
                elif apmhipod_in_bottom_goal is None:
                    # Will need to go down one more step
                    steps_needed = 1
                else:
                    # Will need to go out and then back down
                    steps_needed = 5
            else:
                # Will need to go down
                steps_needed = 1
        else:
            # Will need to go out, sideways and down
            steps_needed = abs(r-1) + abs(c - goal_cols[a]) + 1
        score += steps_needed * energy_costs[a]
    return score

def print_map(tiles, amphipods):
    for r in range(len(lines)):
        for c in range(len(lines[0])):
            if amphipod := amphipods.get((r, c)):
                print(amphipod, end='')
            elif tile := tiles.get((r, c)):
                if tile.can_stop:
                    print('.', end='')
                else:
                    print(' ', end='')
            else:
                print('#', end='')
        if r == 1:
            print(f': {cheap_score(amphipods)}+')
        else:
            print()

def get_state_key(amphipods):
    return tuple(sorted((a, rc) for rc, a in amphipods.items()))

print_map(tiles, amphipods)
print(get_state_key(amphipods))

def do_steps(state, a, r, c, banned_direction, energy):
    energy += energy_costs[a]
    for dr, dc in neighbor_coords:
        if (dr, dc) == banned_direction:
            continue
        new_r = r + dr
        new_c = c + dc
        new_coords = new_r, new_c
        if new_coords in state:
            continue
        tile = tiles.get(new_coords)
        if tile is None:
            continue
        new_state = state.copy()
        new_state[new_coords] = a
        if tile.can_stop:
            yield energy, new_state
        yield from do_steps(state, a, new_r, new_c, (-dr, -dc), energy)

def next_states(amphipods):
    for r, c in amphipods:
        state = amphipods.copy()
        a = state.pop((r, c))
        yield from do_steps(state, a, r, c, None, 0)


for energy, next_state in next_states(amphipods):
    print_map(tiles, next_state)
    print(energy)

integers = itertools.count()

# (total estimate, energy used to come here, unique int, key, state)
to_explore = [
    (cheap_score(amphipods), 0, next(integers), get_state_key(amphipods), amphipods)
]
# state key => energy used to come here
cheapest_paths = {}

print_counter = 0
while to_explore:
    estimate, energy, _, key, amphipods = heapq.heappop(to_explore)
    print_counter += 1
    if print_counter > 1000:
        print_counter = 0
        print(len(to_explore), len(cheapest_paths), estimate)
        print_map(tiles, amphipods)
    if estimate == energy:
        print()
        print_map(tiles, amphipods)
        print('Part 1:', energy)
        break
    for used_energy, next_amphipods in next_states(amphipods):
        next_energy = energy + used_energy
        key = get_state_key(next_amphipods)
        if key not in cheapest_paths or next_energy < cheapest_paths[key]:
            # Found a new cheapest way to get to this state!
            cheapest_paths[key] = next_energy
            #print(key, next_energy)
            heapq.heappush(
                to_explore,
                (
                    next_energy + cheap_score(next_amphipods),
                    next_energy,
                    next(integers),
                    key,
                    next_amphipods,
                )
            )
