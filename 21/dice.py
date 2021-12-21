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
