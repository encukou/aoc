from functools import cached_property
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

def strongest_bridge(start_bridge, start_score, components, start_pins):
    best_score = 0
    best_bridge = []
    for component in components:
        if start_pins in component.ports:
            new_score, new_bridge = strongest_bridge(
                start_bridge + [component], start_score + component.strength,
                components - {component},
                component.other_port(start_pins),
            )
            new_score += component.strength
            new_bridge = [component] + new_bridge
            if new_score > best_score:
                best_score, best_bridge = new_score, new_bridge
    if best_bridge == []:
        print(len(start_bridge), len(components), start_bridge,
              start_score, start_pins)
    return best_score, best_bridge

best_score, best_bridge = strongest_bridge([], 0, all_components, 0)
print(best_score, best_bridge)

print('*** part 1:', best_score)




print('*** part 2:', ...)
