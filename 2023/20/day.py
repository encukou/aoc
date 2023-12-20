import sys
from dataclasses import dataclass, field
from collections import deque, defaultdict
from functools import cached_property
from pprint import pprint
import math

data = sys.stdin.read().splitlines()
print(data)

@dataclass
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

    def _send_all(self, is_high, payload=None):
        yield from (
            Pulse(is_high, self.name, dst, payload)
            for dst in self.connected_names
        )

@dataclass
class FlipFlop(Module):
    is_high: bool = False

    def receive(self, pulse):
        if not pulse.is_high:
            self.is_high = not self.is_high
            yield from self._send_all(self.is_high)

    def __repr__(self):
        return f'{self.name}[{"^" if self.is_high else "_"}'

class Conjunction(Module):
    def receive(self, pulse):
        self.memory[pulse.src] = pulse.is_high
        yield from self._send_all(
            not all(self.memory.values()),
            pulse.src if pulse.is_high else None,
        )

    @cached_property
    def memory(self):
        memory = {}
        for module in self._network.modules.values():
            if self.name in module.connected_names:
                memory[module.name] = False
        return memory

    def __repr__(self):
        return f'{self.name}[{"".join("_^"[v] for v in self.memory.values())}]'

class Broadcaster(Module):
    def receive(self, pulse):
        yield from self._send_all(pulse.is_high)

    def __repr__(self):
        return f'{self.name}[>]'

class Output(Module):
    prev_module = None
    def receive(self, pulse):
        if pulse.payload is None:
            return ()
        print(pulse, pulse.payload)

        # assert only one module is connected to this one
        prev_module = self._network.modules[pulse.src]
        assert self.prev_module in (None, prev_module)
        self.prev_module = prev_module

        self.preoutput_trigger_times[pulse.payload].append(
            self._network.num_pushes)

        print(self._network.num_pushes, self._network)
        pprint(self.preoutput_trigger_times)
        times_lengths = []
        for times in self.preoutput_trigger_times.values():
            assert all(
                time == i * times[0]
                for i, time in enumerate(times, start=1)
            )
            times_lengths.append(len(times))
        if all(tl > 7 for tl in times_lengths):
            print('*** part 2:', math.lcm(*(t[0] for t in self.preoutput_trigger_times.values())))
            exit()

        return ()

    @cached_property
    def preoutput_trigger_times(self):
        return defaultdict(list)

MOD_CLASSES = {'%': FlipFlop, '&': Conjunction}

@dataclass(slots=True)
class Pulse:
    is_high: bool
    src: str
    dest: str
    payload: str = None

    def __repr__(self):
        return f'{self.src} -{("low", "high")[self.is_high]}-> {self.dest}'

class ModuleNetwork:
    preoutput = None

    def __init__(self, data):
        self.modules = {'rx': Output('rx', (), self)}
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
            print(self.num_pushes, self)

    def __repr__(self):
        return ' '.join(
            repr(m) for m in self.modules.values()
            if isinstance(m, Conjunction)
        )

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
