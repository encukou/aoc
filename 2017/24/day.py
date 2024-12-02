from functools import cached_property, lru_cache
import sys

data = sys.stdin.read().splitlines()
print(data)

class Component:
    def __init__(self, line):
        self.ports = tuple(sorted(int(n) for n in line.split('/')))

    def __repr__(self):
        return '<' + '/'.join(str(p) for p in self.ports) + '>'

    @cached_property
    def strength(self):
        return sum(self.ports)

    def other_port(self, pins):
        if self.ports[0] == pins:
            return self.ports[1]
        return self.ports[0]

all_components = frozenset(Component(line) for line in data)
print(all_components)

@lru_cache
def strongest_bridge(components, start_pins):
    best_score = 0
    best_bridge = []
    for component in components:
        if start_pins in component.ports:
            new_score, new_bridge = strongest_bridge(
                components - {component},
                component.other_port(start_pins),
            )
            new_score += component.strength
            new_bridge = [component] + new_bridge
            if new_score > best_score:
                best_score, best_bridge = new_score, new_bridge
    return best_score, best_bridge

best_score, best_bridge = strongest_bridge(all_components, 0)
print(best_score, best_bridge)

print('*** part 1:', best_score)


@lru_cache
def longest_bridge(components, start_pins):
    best_score = 0, 0
    best_bridge = []
    for component in components:
        if start_pins in component.ports:
            new_length, new_strength, new_bridge = longest_bridge(
                components - {component},
                component.other_port(start_pins),
            )
            new_length += 1
            new_strength += component.strength
            new_bridge = [component] + new_bridge
            new_score = new_length, new_strength
            if new_score > best_score:
                best_score, best_bridge = new_score, new_bridge
    return (*best_score, best_bridge)

best_length, best_strength, best_bridge = longest_bridge(all_components, 0)
print(best_score, best_bridge)

print('*** part 2:', best_strength)
