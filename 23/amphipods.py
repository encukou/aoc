import itertools
import heapq

import numpy

with open('data.txt') as f:
    lines = [line.rstrip() for line in f]

if True:
    # Part 2:
    lines.insert(3, "  #D#C#B#A#")
    lines.insert(4, "  #D#B#A#C#")

for i, line in enumerate(lines):
    lines[i] = line.ljust(len(lines[0]))

neighbor_coords = [(0,1), (0,-1), (1,0), (-1,0)]
energy_costs = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}

room_cols = {}
room_rows = set()

valid_positions = set()
amphipods = {}
for r, line in enumerate(lines):
    goals = iter('ABCD')
    for c, char in enumerate(line):
        if char in ' #':
            continue
        if char == '.':
            can_stop = all(line[c] in ' .#' for line in lines)
            corridor_row = r
        else:
            room_cols[next(goals)] = c
            room_rows.add(r)
            can_stop = True
            amphipods[r, c] = char
        valid_positions.add((r, c))

room_rows = sorted(room_rows)
room_cols_v = set(room_cols.values())

def cheap_score(amphipods):
    score = 0
    for (r, c), a in amphipods.items():
        steps_needed = 0
        if c == room_cols[a]:
            if all(amphipods.get((R, c)) ==a for R in room_rows if R > r):
                # Already in place
                continue
            else:
                # Will need to go out and then back down
                steps_needed = 3 + abs(r - corridor_row)
        else:
            # Will need to go out, sideways and down
            steps_needed = abs(r-corridor_row) + abs(c - room_cols[a]) + 1
        score += steps_needed * energy_costs[a]
    return score

def print_map(amphipods):
    for r in range(len(lines)):
        for c in range(len(lines[0])):
            if amphipod := amphipods.get((r, c)):
                print(amphipod, end='')
            elif (r, c) in valid_positions:
                if c in room_cols:
                    print(' ', end='')
                else:
                    print('.', end='')
            else:
                print('#', end='')
        if r == 1:
            print(f': {cheap_score(amphipods)}+')
        else:
            print()

def get_state_key(amphipods):
    return tuple(sorted((a, rc) for rc, a in amphipods.items()))

print_map(amphipods)
print(get_state_key(amphipods))

def do_steps(state, a, r, c, energy):
    steps = 0
    # The amphipod can:
    # 1. move out of a room into the hallway
    # 2. move out of the hallway into a room
    goal = room_cols.get(c)
    if goal == a and all(amphipods.get((R, c)) == a for R in room_rows if R > r):
        # Already in place; won't move further
        return
    # Must move out
    if any(amphipods.get((R, c)) for R in room_rows if R < r):
        # blocked!
        return
    out_steps = abs(r - corridor_row)
    # Can move left or right along the corridor
    for direction in 1, -1:
        for distance in range(len(lines[0])):
            new_c = c + distance * direction
            if (corridor_row, new_c) not in valid_positions:
                break
            if (corridor_row, new_c) in state:
                break
            if new_c not in room_cols_v:
                if out_steps:
                    # Can stop here
                    new_state = state.copy()
                    new_state[corridor_row, new_c] = a
                    yield (
                        energy + (out_steps + distance) * energy_costs[a],
                        new_state,
                    )
            elif room_cols[a] == new_c:
                # Can move down
                for R in reversed(room_rows):
                    occupant = state.get((R, new_c))
                    if occupant is None:
                        new_state = state.copy()
                        new_state[R, new_c] = a
                        in_steps = abs(corridor_row - R)
                        yield (
                            energy
                            + (out_steps + distance + in_steps)
                                * energy_costs[a],
                            new_state,
                        )
                    elif occupant != a:
                        break

def next_states(amphipods):
    for r, c in amphipods:
        state = amphipods.copy()
        a = state.pop((r, c))
        yield from do_steps(state, a, r, c, 0)


for energy, next_state in next_states(amphipods):
    print_map(next_state)
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
        print_map(amphipods)
    if estimate == energy:
        print()
        print_map(amphipods)
        print('Minimum energy:', energy)
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
