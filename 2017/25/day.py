import sys
import re

data = sys.stdin.read().splitlines()

class Machine:
    def __init__(self):
        self.rules = {}
        self.tape = set()
        self.position = 0

    def run(self, n):
        self.dump(None)
        for i in range(n):
            self.step()
            if i < 10 or i % 2**8 == 0:
                self.dump(i)

    def dump(self, n):
        print(n, self.position, self.state, self.diagnostic)

    def step(self):
        transition = self.rules[self.state].transitions[self.position in self.tape]
        if transition.value:
            self.tape.add(self.position)
        else:
            self.tape.discard(self.position)
        self.position += transition.direction
        self.state = transition.next_state

    @property
    def diagnostic(self):
        return len(self.tape)

class Rule:
    def __init__(self):
        self.transitions = {}

class Transition:
    def __init__(self):
        pass

def make_machine(data):
    machine = Machine()
    for line in data:
        if not line:
            continue
        print(line)
        if m := re.fullmatch('Begin in state (.*).', line):
            machine.state = m[1]
        elif m := re.fullmatch('Perform a diagnostic checksum after (.*) steps.', line):
            machine.steps_until_checkup = int(m[1])
        elif m := re.fullmatch('In state (.*):', line):
            current_rule = machine.rules[m[1]] = Rule()
        elif m := re.fullmatch(' *If the current value is (.*):', line):
            current_transition = current_rule.transitions[int(m[1])] = Transition()
        elif m := re.fullmatch(' *- Write the value (.*).', line):
            current_transition.value = int(m[1])
        elif m := re.fullmatch(' *- Move one slot to the (.*).', line):
            current_transition.direction = {'left': -1, 'right': +1}[m[1]]
        elif m := re.fullmatch(' *- Continue with state (.*).', line):
            current_transition.next_state = m[1]
        else:
            raise ValueError(line)
    return machine

machine = make_machine(data)
machine.run(machine.steps_until_checkup)

print('*** part 1:', machine.diagnostic)




print('*** part 2:', ...)
