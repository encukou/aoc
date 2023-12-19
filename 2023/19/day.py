import sys
import dataclasses
import operator
from functools import cached_property
from pprint import pprint

data = sys.stdin.read().splitlines()
print(data)

OPS = {
    '<': operator.lt,
    '>': operator.gt,
}

@dataclasses.dataclass
class Condition:
    category: str
    op: callable
    value: int

    @classmethod
    def parse(cls, spec):
        return cls(spec[0], OPS[spec[1]], int(spec[2:]))

    def evaluate(self, part):
        return self.op(part.categories[self.category], self.value)

@dataclasses.dataclass
class Rule:
    condition: Condition | None
    destination: str

    @classmethod
    def parse(cls, spec):
        try:
            cond, destination = spec.split(':')
        except ValueError:
            return cls(None, spec)
        return cls(Condition.parse(cond), destination)

    def evaluate(self, part):
        if not self.condition:
            return True
        return self.condition.evaluate(part)

    @cached_property
    def is_final(self):
        return self.destination in 'AR'

@dataclasses.dataclass
class Workflow:
    name: str
    rules: list['Rule']

    @classmethod
    def parse(cls, line):
        name, rest = line.removesuffix('}').split('{')
        rules = [Rule.parse(part) for part in rest.split(',')]
        return cls(name, rules)

    def simplify(self, workflows):
        while (
            len(self.rules) > 1
            and self.rules[-2].destination == self.rules[-1].destination
        ):
            del self.rules[-2]
        if len(self.rules) == 1:
            [remaining_rule] = self.rules
            assert remaining_rule.condition is None
            for name, wf in workflows.items():
                wf.replace_destination(
                    self.name, remaining_rule.destination, workflows,
                )

    def replace_destination(self, src, dst, workflows):
        changed = False
        for rule in self.rules:
            if rule.destination == src:
                rule.destination = dst
                changed = True
        if changed:
            self.simplify(workflows)

    def classify_part(self, part, workflows):
        for rule in self.rules:
            if rule.evaluate(part):
                if rule.is_final:
                    return rule.destination
                return workflows[rule.destination].classify_part(part, workflows)

@dataclasses.dataclass
class Part:
    categories: dict[str, int]

    @classmethod
    def parse(cls, line):
        categories = {}
        for spec in line.removeprefix('{').removesuffix('}').split(','):
            name, value = spec.split('=')
            categories[name] = int(value)
        return cls(categories)


it = iter(data)

workflows = {}
for line in it:
    if not line:
        break
    wf = Workflow.parse(line)
    workflows[wf.name] = wf
parts = []
for line in it:
    parts.append(Part.parse(line))
#pprint(parts)

for wf in workflows.values():
    wf.simplify(workflows)
print(len(workflows))
workflows = {name: wf for name, wf in workflows.items() if len(wf.rules) > 1}
pprint(workflows)
print(len(workflows))

total = 0
in_wf = workflows['in']
for part in parts:
    result = in_wf.classify_part(part, workflows)
    print(part, result)
    if result == 'A':
        total += sum(part.categories.values())

print('*** part 1:', total)

print('*** part 2:', ...)
