import collections
import heapq
import re

positions = []

for line in """
    Player 1 starting position: 10
    Player 2 starting position: 9
""".strip().splitlines():
    match = re.fullmatch(r'\s*Player \d+ starting position: (\d+)\s*', line)
    positions.append(int(match[1]) - 1)


class DeterministicDiracDie:
    value = 0
    rolls = 0

    def roll(self):
        self.rolls += 1
        self.value %= 100
        self.value += 1
        return self.value

print(positions)

def play(positions, die):
    positions = list(positions)
    scores = [0 for p in positions]
    while True:
        for player_number in range(2):
            for roll_number in range(3):
                positions[player_number] += die.roll()
            positions[player_number] %= 10
            scores[player_number] += positions[player_number] + 1
            if scores[player_number] >= 1000:
                 return player_number, positions, scores, die.rolls

winner, new_positions, scores, rolls = play(positions, DeterministicDiracDie())
print(f'{winner} wins, positions: {new_positions}, scores: {scores}, rolls: {rolls}')

print('Part 1:', rolls * scores[1-winner])

three_roll_outcome_counts = tuple(collections.Counter(
    a + b + c
    for a in range(1, 4)
    for b in range(1, 4)
    for c in range(1, 4)
).items())
print(three_roll_outcome_counts)

universes = [(0, 0, 0, *positions, 0)]
universe_counts = {(0, 0, *positions, 0): 1}
wins = [0, 0]

print_counter = 0
while universes:
    current_entry = heapq.heappop(universes)
    total_score = current_entry[0]
    current_universe = (*current_entry[1:], )
    count = universe_counts.pop(current_universe)
    #print('<-', current_universe, count)
    if print_counter % 2021 == 0:
        print(
            total_score,
            current_universe,
            [len(str(w)) for w in wins],
            len(universes),
            count,
        )
        print_counter = 0
    print_counter += 1
    for roll_sum, roll_count in three_roll_outcome_counts:
        new_universe = list(current_universe)
        player_number = new_universe[-1]
        new_universe[player_number+2] += roll_sum
        new_universe[player_number+2] %= 10
        new_universe[player_number] += new_universe[player_number+2] + 1
        new_universe[-1] = 1 - player_number
        if new_universe[player_number] >= 21:
            wins[player_number] += count * roll_count
            #print('!!')
        else:
            new_tuple = tuple(new_universe)
            new_count = count * roll_count
            if new_tuple in universe_counts:
                universe_counts[new_tuple] += new_count
                #print('++', new_tuple, '*', new_count)
            else:
                universe_counts[new_tuple] = new_count
                total_score = new_universe[0] + new_universe[1]
                heapq.heappush(universes, (total_score, *new_tuple))
                #print('->', new_tuple, '*', new_count)

print(wins)
print('Part 2:', max(wins))
