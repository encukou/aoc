import sys
from dataclasses import dataclass, field
from collections import deque
from functools import cached_property
import math

data = sys.stdin.read().splitlines()
print(data)

@dataclass(slots=True)
class Module:
    name: str
    connected_names: list[str]
    _network: 'ModuleNetwork' = field(repr=False)

    @classmethod
    def parse(cls, spec, network):
        name, connected_spec = spec.split('->')
        name = name.strip()
        subclass = MOD_CLASSES.get(name[0])
        if subclass:
            cls = subclass
            name = name[1:]
        else:
            cls = Broadcaster
        connected_names = [n.strip() for n in connected_spec.split(',')]
        return cls(name, connected_names, network)

    def _send_all(self, is_high):
        yield from (
            Pulse(is_high, self.name, dst)
            for dst in self.connected_names
        )

@dataclass(slots=True)
class FlipFlop(Module):
    is_high: bool = False

    def receive(self, pulse):
        if not pulse.is_high:
            self.is_high = not self.is_high
            yield from self._send_all(self.is_high)

    def __repr__(self):
        return '[^]' if self.is_high else '[_]'

class Conjunction(Module):
    def receive(self, pulse):
        self.memory[pulse.src] = pulse.is_high
        yield from self._send_all(not all(self.memory.values()))

    @cached_property
    def memory(self):
        memory = {}
        for module in self._network.modules.values():
            if self.name in module.connected_names:
                memory[module.name] = False
        return memory

    def __repr__(self):
        return f'[{"".join("_^"[v] for v in self.memory.values())}]'

class Broadcaster(Module):
    def receive(self, pulse):
        yield from self._send_all(pulse.is_high)

    def __repr__(self):
        return f'[>]'

class Output(Module):
    def receive(self, pulse):
        if not pulse.is_high:
            exit('*** part 2:', self._network.num_pushes)
        return ()

MOD_CLASSES = {'%': FlipFlop, '&': Conjunction}

@dataclass(slots=True)
class Pulse:
    is_high: bool
    src: str
    dest: str

    def __repr__(self):
        return f'{self.src} -{("low", "high")[self.is_high]}-> {self.dest}'

class ModuleNetwork:
    def __init__(self, data):
        self.modules = {}
        for line in data:
            module = Module.parse(line, self)
            self.modules[module.name] = module
        self.pulse_counts = {True: 0, False: 0}
        self.num_pushes = 0

    def push(self):
        self.num_pushes += 1
        sent_pulses = deque([Pulse(False, 'button', 'broadcaster')])
        while sent_pulses:
            pulse = sent_pulses.popleft()
            if self.num_pushes < 100:
                print(pulse)
            self.pulse_counts[pulse.is_high] += 1
            if mod := self.modules.get(pulse.dest):
                sent_pulses.extend(mod.receive(pulse))
        if self.num_pushes < 1000 or self.num_pushes % 777 == 0:
            print(self.num_pushes, self.modules)

def handle_pulses(data, num_iterations):
    network = ModuleNetwork(data)
    for i in range(num_iterations):
        network.push()
    return math.prod(network.pulse_counts.values())

assert handle_pulses("""
broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a
""".strip().splitlines(), 1000) == 32000000

print('*** part 1:', handle_pulses(data, 1000))

if len(data) > 50:
    network = ModuleNetwork(data)
    while True:
        network.push()
