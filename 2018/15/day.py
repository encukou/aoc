import dataclasses
import collections
from functools import cached_property
from textwrap import dedent
import sys

data = sys.stdin.read().splitlines()
print(data)

RESET = '\x1b[0m'
DIRS = {
    '^': (-1, 0),
    '>': (0, 1),
    '<': (0, -1),
    'v': (1, 0),
}

GOBLIN_STRENGTH = 3

@dataclasses.dataclass
class Unit:
    r: int
    c: int
    team: str
    name: str
    strength: int
    hp: int = 200

    @property
    def team_color(self):
        if self.team == 'E':
            return '\x1b[46m'
        elif self.team == 'G':
            return '\x1b[41m'
        return ''

    @cached_property
    def colored_name(self):
        return self.team_color + self.team + self.name + RESET

    def __repr__(self):
        return f'<{self.colored_name} @ {self.r},{self.c} ({self.hp})>'

class End(Exception):
    """The simulation is over."""

@dataclasses.dataclass
class Cave:
    walls: set
    size_r: int
    size_c: int
    units: dict
    turn_number: int = 0
    verbose: bool = True
    end: int = None

    quiet: bool = False

    def draw(self):
        print(f'{'':3}|', end=RESET)
        for c in range(self.size_r):
            print(end=f'{c:2}')
        print()
        for r in range(self.size_r):
            print(f'{r:3}|', end=RESET)
            units = []
            for c in range(self.size_r):
                pos = r, c
                if unit := self.units.get(pos):
                    print(end=unit.colored_name)
                    units.append(unit)
                elif pos in self.walls:
                    print('\x1b[47m', end='##')
                else:
                    print(end='· ')
                print(end=RESET)
            if units:
                print(end='  ')
            for unit in units:
                print(f' {unit.colored_name}({unit.hp})', end='')
            print()

    def step(self):
        verbose = self.verbose
        moves = 0
        attacks = 0
        kills = 0
        for (r, c), unit in sorted(self.units.items()):
            if unit.hp <= 0:
                continue
            if verbose:
                print(f' :{unit}')
            def find_enemy_in_range(r, c, unit):
                candidates = []
                for dr, dc in DIRS.values():
                    enemy = self.units.get((r+dr, c+dc))
                    if enemy and enemy.team != unit.team:
                        candidates.append((enemy.hp, enemy.r, enemy.c, enemy))
                if candidates:
                    candidates.sort()
                    return candidates[0][-1]
            def choose_square(unit):
                to_visit = collections.deque([(unit.r, unit.c, 0)])
                visited = {}
                visited_by_distance = collections.defaultdict(list)
                while to_visit:
                    r, c, distance = to_visit.popleft()
                    pos = r, c
                    if pos in self.walls:
                        continue
                    if pos in visited:
                        continue
                    enemy = self.units.get(pos)
                    if enemy and enemy != unit:
                        if enemy.team != unit.team:
                            nearest = sorted(
                                (r, c) for r, c
                                in visited_by_distance[distance - 1]
                                if find_enemy_in_range(r, c, unit)
                            )
                            nearest.sort()
                            return nearest[0]
                        continue
                    visited[pos] = distance
                    visited_by_distance[distance].append(pos)
                    for dr, dc in DIRS.values():
                        to_visit.append((r+dr, c+dc, distance+1))
            def choose_step(unit, sq):
                to_visit = collections.deque([(*sq, 0)])
                visited = {}
                visited_by_distance = collections.defaultdict(list)
                while to_visit:
                    r, c, distance = to_visit.popleft()
                    pos = r, c
                    if pos in self.walls:
                        continue
                    if pos in visited:
                        continue
                    other = self.units.get(pos)
                    if other:
                        if other == unit:
                            nearest = sorted(
                                (r, c) for r, c
                                in visited_by_distance[distance - 1]
                                if abs(r-unit.r)+abs(c-unit.c) == 1
                            )
                            return nearest[0]
                        continue
                    visited[pos] = distance
                    visited_by_distance[distance].append(pos)
                    for dr, dc in DIRS.values():
                        to_visit.append((r+dr, c+dc, distance+1))
            enemy = find_enemy_in_range(r, c, unit)
            if verbose:
                print(f'   - {enemy=}')
            if not enemy:
                if not any(u.team != unit.team for u in self.units.values()):
                    self.end = self.turn_number
                    print(f'Combat ends after {self.end} full rounds')
                    self.remainig_hp = sum(u.hp for u in self.units.values())
                    team = next(iter(self.units.values())).team
                    print(f'{team} win with {self.remainig_hp} total hit points left')
                    print(f'Outcome: {self.get_score()}')
                    print(f'Kills: {self.team_kills}')
                sq = choose_square(unit)
                if verbose:
                    print(f'   - {sq=}')
                if not sq:
                    continue
                step = choose_step(unit, sq)
                if verbose:
                    print(f'   - {step=}')
                if step:
                    self.move_unit(unit, step)
                    moves += 1
                enemy = find_enemy_in_range(unit.r, unit.c, unit)
                if verbose:
                    print(f'   - {enemy=}')
            if enemy:
                self.hit(unit, enemy)
                attacks += 1
                if enemy.hp <= 0:
                    kills += 1
        self.turn_number += 1
        print(f'{self.turn_number}: {moves=} {attacks=} {kills=}')
        if not self.quiet:
            self.verbose = moves or kills or any(u.hp < 20 for u in self.units.values())
        if self.verbose:
            self.draw()
            print(f'Turn {self.turn_number+1} to start.', flush=True)
        return moves, attacks, kills

    def hit(self, attacker, defender):
        defender.hp -= attacker.strength
        if defender.hp <= 0:
            pos = defender.r, defender.c
            self.units.pop(pos, None)
            self.team_kills.add(defender.team)

    def move_unit(self, unit, new_pos):
        assert new_pos not in self.units
        assert new_pos not in self.walls
        u = self.units.pop((unit.r, unit.c))
        assert u is unit
        unit.r, unit.c = new_pos
        self.units[new_pos] = unit

    def get_score(self):
        return self.end * self.remainig_hp

    @classmethod
    def from_data(cls, data, elf_strength=GOBLIN_STRENGTH, quiet=False):
        next_name = iter(
            'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        ).__next__
        self = cls(set(), len(data), len(data[0]), {}, quiet=quiet)
        for r, line in enumerate(data):
            for c, char in enumerate(line):
                pos = r, c
                match char:
                    case '#':
                        self.walls.add(pos)
                    case 'G':
                        self.units[pos] = Unit(
                            r, c, char, next_name(), GOBLIN_STRENGTH)
                    case 'E':
                        self.units[pos] = Unit(
                            r, c, char, next_name(), elf_strength)
                    case '.':
                        pass
                    case _:
                        raise ValueError(char)
        self.team_kills = set()
        return self

    def simulate(self):
        self.verbose = not self.quiet
        self.draw()
        while self.end is None:
            self.step()
        self.draw()

def solve(data):
    cave = Cave.from_data(data, elf_strength=3)
    cave.simulate()
    part1_score = cave.get_score()

    low = 1
    high = 200
    while low < high-1:
        mid = (low + high) // 2
        cave = Cave.from_data(data, elf_strength=mid)
        cave.simulate()
        elves_died = 'E' in cave.team_kills
        summary = 'some died' if elves_died else 'survived'
        print(f'Elves had {mid} attack and {summary}. Checking {low}-{high}.')
        if elves_died:
            low = mid
        else:
            high = mid
            part2_score = cave.get_score()

    print(f'Elves need {high} attack for score of {part2_score}')
    return part1_score, part2_score

print('*** part 1:', solve(data)[0])

if len(data) < 10:
    assert solve(dedent("""
    #######
    #G..#E#
    #E#E.E#
    #G.##.#
    #...#E#
    #...E.#
    #######
    """).strip().splitlines())[0] == 36334
    assert solve(dedent("""
    #######
    #E..EG#
    #.#G.E#
    #E.##E#
    #G..#.#
    #..E#.#
    #######
    """).strip().splitlines()) == (39514, 31284)
    assert solve(dedent("""
    #######
    #.E...#
    #.#..G#
    #.###.#
    #E#G#G#
    #...#G#
    #######
    """).strip().splitlines()) == (28944, 6474)
    assert solve(dedent("""
    #########
    #G......#
    #.E.#...#
    #..##..G#
    #...##..#
    #...#...#
    #.G...G.#
    #.....G.#
    #########
    """).strip().splitlines()) == (18740, 1140)




print('*** part 2:', solve(data)[1])
