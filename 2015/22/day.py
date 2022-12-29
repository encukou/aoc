import sys
from dataclasses import dataclass, field, replace
from pprint import pprint
from heapq import heappush, heappop

data = sys.stdin.read().strip().splitlines()

boss_attrs = {}
for line in data:
    name, value = line.split(':')
    boss_attrs[name.replace(' ', '').lower()] = int(value)

print('boss:', boss_attrs)

@dataclass(frozen=True, order=True)
class State:
    mana_spent: int
    hero_hp: int
    hero_mana: int
    boss_hp: int
    shield_counter: int
    poison_counter: int
    recharge_counter: int
    boss_damage: int
    hero_fatigue: int
    prev: 'State' = field(compare=False, repr=False)
    messages: list = field(compare=False, repr=False)

    def __repr__(self):
        return f'<[spent={self.mana_spent} HP {self.hero_hp}:{self.boss_hp} M={self.hero_mana} S{self.shield_counter} P{self.poison_counter} R{self.recharge_counter}>'

    def gen_next(self):
        MM_COST = 53
        args = {}
        messages = []
        def start_turn(state):
            if state.shield_counter:
                state = replace(state, shield_counter=state.shield_counter-1)
            if state.poison_counter:
                state = replace(
                    state,
                    poison_counter=state.poison_counter-1,
                    boss_hp=state.boss_hp-3,
                )
            if state.recharge_counter:
                state = replace(
                    state,
                    recharge_counter=state.recharge_counter-1,
                    hero_mana=state.hero_mana+101,
                )
            return state
        def finalize_turn(spell_name, **kwargs):
            fin_messages = list(messages)
            fin_messages.append(f'Hero used {spell_name}!')
            midturn = start_turn(replace(initial, **kwargs))
            if midturn.boss_hp > 0:
                # Boss attacks
                armor = 7 if midturn.shield_counter else 0
                damage = max(1, self.boss_damage - armor)
                final = replace(midturn, hero_hp=midturn.hero_hp - damage)
                fin_messages.append(f'Boss does {damage} damage!')
            else:
                final = midturn
            return replace(
                final,
                prev=self,
                messages=fin_messages,
            )
        initial = replace(self, hero_hp=self.hero_hp - self.hero_fatigue)
        initial = start_turn(initial)
        if initial.hero_hp <= 0:
            # Lose...
            return
        # Magic Missile
        if initial.hero_mana > MM_COST:
            boss_hp = initial.boss_hp - 4
            yield finalize_turn(
                spell_name='Magic Missile',
                boss_hp=boss_hp,
                hero_mana=initial.hero_mana - MM_COST,
                mana_spent=initial.mana_spent+MM_COST,
            )
        # Drain
        DRAIN_COST = 73
        if initial.hero_mana > DRAIN_COST:
            boss_hp = initial.boss_hp - 2
            hero_hp = initial.hero_hp + 2
            yield finalize_turn(
                spell_name='Drain',
                boss_hp=boss_hp,
                hero_hp=hero_hp,
                hero_mana=initial.hero_mana - DRAIN_COST,
                mana_spent=initial.mana_spent + DRAIN_COST,
            )
        # Shield
        SHIELD_COST = 113
        if initial.hero_mana > SHIELD_COST and not initial.shield_counter:
            yield finalize_turn(
                spell_name='Shield',
                shield_counter=6,
                hero_mana=initial.hero_mana - SHIELD_COST,
                mana_spent=initial.mana_spent + SHIELD_COST,
            )
        # Poison
        POISON_COST = 173
        if initial.hero_mana > POISON_COST and not initial.poison_counter:
            yield finalize_turn(
                spell_name='Poison',
                poison_counter=6,
                hero_mana=initial.hero_mana - POISON_COST,
                mana_spent=initial.mana_spent + POISON_COST,
            )
        # Recharge
        RECHARGE_COST = 229
        if initial.hero_mana > RECHARGE_COST and not initial.recharge_counter:
            yield finalize_turn(
                spell_name='Recharge',
                recharge_counter=5,
                hero_mana=initial.hero_mana - RECHARGE_COST,
                mana_spent=initial.mana_spent + RECHARGE_COST,
            )

    def print_history(self):
        if self.prev:
            self.prev.print_history()
            for msg in self.messages:
                print('- ', msg)
        print(self)

def simulate(hero_hp, hero_mana, boss_hp, boss_damage, hard=False):
    to_visit = [State(
        mana_spent=0,
        hero_hp=hero_hp,
        hero_mana=hero_mana,
        boss_hp=boss_hp,
        boss_damage=boss_damage,
        shield_counter=0,
        poison_counter=0,
        recharge_counter=0,
        hero_fatigue=int(hard),
        prev=None,
        messages=None,
    )]
    visited = set()
    while to_visit:
        node = heappop(to_visit)
        if node in visited:
            continue
        visited.add(node)
        print(node)
        if node.boss_hp <= 0:
            print('Win!')
            node.print_history()
            print(f'Boss slain! {node.mana_spent} mana spent!')
            return node.mana_spent
        for n in node.gen_next():
            if n.hero_hp > 0:
                heappush(to_visit, n)
    else:
        print('lost...')
        node.print_history()
        print('Hero slain...')

MM=53
D=73
S=113
P=173
R=229
assert simulate(10, 250, 13, 8) == P+MM
assert simulate(10, 250, 14, 8) == R+S+D+P+MM,R+S+D+P+MM

result = simulate(50, 500, boss_attrs['hitpoints'], boss_attrs['damage'])
print(f'*** part 1: {result}')

result = simulate(50, 500, boss_attrs['hitpoints'], boss_attrs['damage'], hard=True)
print(f'*** part 2: {result}')
