import sys
from dataclasses import dataclass
from pprint import pprint
import itertools

@dataclass(order=True)
class Item:
    name: str
    cost: int
    damage: int
    armor: int

    def __bool__(self):
        return bool(self.cost)

@dataclass
class Actor:
    name: str
    hitpoints: int
    damage: int
    armor: int

data = sys.stdin.read().strip().splitlines()

boss_attrs = {}
for line in data:
    name, value = line.split(':')
    boss_attrs[name.replace(' ', '').lower()] = int(value)

shop = {}
for line in """
Weapons:    Cost  Damage  Armor
Dagger        8     4       0
Shortsword   10     5       0
Warhammer    25     6       0
Longsword    40     7       0
Greataxe     74     8       0

Armor:      Cost  Damage  Armor
Leather      13     0       1
Chainmail    31     0       2
Splintmail   53     0       3
Bandedmail   75     0       4
Platemail   102     0       5

Rings:      Cost  Damage  Armor
Damage +1    25     1       0
Damage +2    50     2       0
Damage +3   100     3       0
Defense +1   20     0       1
Defense +2   40     0       2
Defense +3   80     0       3
""".strip().splitlines():
    if ':' in line:
        category, attributes = line.split(':')
        shop[category] = []
    elif line:
        name, *attributes = line.rsplit(None, 3)
        shop[category].append(Item(name, *(int(a) for a in attributes)))
nothing = Item('nothing', 0, 0, 0)

builds = []
items = [None] * 4
for items[0] in shop['Weapons']:
    for items[1] in (nothing, *shop['Armor']):
        for i, items[2] in enumerate((nothing, *shop['Rings'])):
            for items[3] in ((nothing, *shop['Rings'][i:])):
                cost = sum(it.cost for it in items)
                damage = sum(it.damage for it in items)
                armor = sum(it.armor for it in items)
                builds.append((cost, damage, armor, tuple(items)))
builds.sort()

def simulate_battle(hero, boss, cost, items):
    actors = (hero, boss)
    print(f'A Sturdy Orc appears, clad in rawhide [DEF={boss.armor}] and wielding a club [DMG={boss.damage}].')
    print(f'The hero prepares, clad in {items[1].name} [DEF={items[1].armor}] and wielding a {items[0].name} [DMG={items[0].damage}].')
    for side, ring in ('left', items[2]), ('right', items[3]):
        if ring:
            print(f"A Ring of {ring.name} glistens on the hero's {side} hand.")
    print(f'That equipment cost {cost} gold!')
    for turn_number in itertools.count(start=1):
        attacker = actors[(turn_number+1) % 2]
        defender = actors[turn_number % 2]
        damage = max(1, attacker.damage - defender.armor)
        defender.hitpoints -= damage
        print(f'[turn {turn_number}] {attacker.name} hits for {damage} damage! {defender.name} is down to {defender.hitpoints} HP!')
        if defender.hitpoints <= 0:
            print(f'{defender.name} is vanquished!')
            return attacker

for cost, damage, armor, items in sorted(builds):
    hero = Actor('Hero', 100, damage, armor)
    boss = Actor('Boss', **boss_attrs)
    simulate_battle(hero, boss, cost, items)
    if hero.hitpoints > 0:
        break

print(f'*** part 1: {cost}')

for cost, damage, armor, items in sorted(builds, reverse=True):
    hero = Actor('Hero', 100, damage, armor)
    boss = Actor('Boss', **boss_attrs)
    simulate_battle(hero, boss, cost, items)
    if boss.hitpoints > 0:
        break

print(f'*** part 2: {cost}')
