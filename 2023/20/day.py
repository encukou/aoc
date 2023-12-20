import sys
from dataclasses import dataclass
from collections import deque
from functools import cached_property
import math

data = sys.stdin.read().splitlines()
print(data)

@dataclass
class Module:
    name: str
    connected_names: list[str]
    _all_modules: dict

    @classmethod
    def parse(cls, spec, modules):
        name, connected_spec = spec.split('->')
        name = name.strip()
        subclass = MOD_CLASSES.get(name[0])
        if subclass:
            cls = subclass
            name = name[1:]
        else:
            cls = Broadcaster
        connected_names = [n.strip() for n in connected_spec.split(',')]
        return cls(name, connected_names, modules)

    def _send_all(self, is_high):
        yield from (
            Pulse(is_high, self.name, dst)
            for dst in self.connected_names
        )

class FlipFlop(Module):
    is_high = False

    def receive(self, pulse):
        if not pulse.is_high:
            self.is_high = not self.is_high
            yield from self._send_all(self.is_high)

class Conjunction(Module):
    def receive(self, pulse):
        self.memory[pulse.src] = pulse.is_high
        yield from self._send_all(not all(self.memory.values()))

    @cached_property
    def memory(self):
        memory = {}
        for module in self._all_modules.values():
            if self.name in module.connected_names:
                memory[module.name] = False
        return memory

class Broadcaster(Module):
    def receive(self, pulse):
        yield from self._send_all(pulse.is_high)

class Output(Module):
    def receive(self, pulse):
        return ()

MOD_CLASSES = {'%': FlipFlop, '&': Conjunction}

@dataclass(slots=True)
class Pulse:
    is_high: bool
    src: str
    dest: str

    def __repr__(self):
        return f'{self.src} -{("low", "high")[self.is_high]}-> {self.dest}'

def handle_pulses(config, num_iterations):
    modules = {}
    for line in config:
        module = Module.parse(line, modules)
        modules[module.name] = module
    sent_pulses = deque()
    counts = {True: 0, False: 0}
    for i in range(num_iterations):
        sent_pulses.append(Pulse(False, 'button', 'broadcaster'))
        while sent_pulses:
            pulse = sent_pulses.popleft()
            print(pulse)
            counts[pulse.is_high] += 1
            if mod := modules.get(pulse.dest):
                sent_pulses.extend(mod.receive(pulse))
    return math.prod(counts.values())

assert handle_pulses("""
broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a
""".strip().splitlines(), 1000) == 32000000

print('*** part 1:', handle_pulses(data, 1000))




print('*** part 2:', ...)
