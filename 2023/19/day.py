import sys
import dataclasses
import operator
from functools import cached_property
import math
from pprint import pprint

#import pysnooper

data = sys.stdin.read().splitlines()
print(data)

OPS = {
    '<': operator.lt,
    '>': operator.gt,
}

@dataclasses.dataclass
class Condition:
    category: str
    op_name: str
    value: int

    @classmethod
    def parse(cls, spec):
        return cls(spec[0], spec[1], int(spec[2:]))

    @cached_property
    def op(self):
        return OPS[self.op_name]

    def __repr__(self):
        return f'{self.category}{self.op_name}{self.value}'

    def evaluate(self, part):
        return self.op(part.categories[self.category], self.value)

    def split_ranges(self, ranges):
        affected_range = ranges[self.category]
        if self.op == operator.lt:
            matched_range = range(affected_range.start, self.value)
            nonmatched_range = range(self.value, affected_range.stop)
        elif self.op == operator.gt:
            nonmatched_range = range(affected_range.start, self.value+1)
            matched_range = range(self.value+1, affected_range.stop)
        else:
            raise ValueError(self.op)
        def _updated_ranges(r):
            if r is None:
                return None
            return ranges | {self.category: r}
        return _updated_ranges(matched_range), _updated_ranges(nonmatched_range)

@dataclasses.dataclass
class Rule:
    condition: Condition | None
    destination_name: str
    workflows: dict[str, 'Workflow'] = dataclasses.field(repr=False)

    @classmethod
    def parse(cls, spec, workflows):
        try:
            cond, destination = spec.split(':')
        except ValueError:
            return cls(None, spec, workflows)
        return cls(Condition.parse(cond), destination, workflows)

    def __repr__(self):
        if self.condition:
            return f'{self.condition}:{self.destination_name}'
        return f':{self.destination_name}'

    def evaluate(self, part):
        if not self.condition:
            return True
        return self.condition.evaluate(part)

    @cached_property
    def is_final(self):
        return self.destination in 'AR'

    @cached_property
    def destination(self):
        return self.workflows[self.destination_name]

    def split_ranges(self, ranges):
        if self.condition:
            return self.condition.split_ranges(ranges)
        return ranges, None

@dataclasses.dataclass
class Workflow:
    name: str
    rules: list['Rule']
    workflows: dict[str, 'Workflow'] = dataclasses.field(repr=False)

    @classmethod
    def parse(cls, line, workflows):
        name, rest = line.removesuffix('}').split('{')
        rules = [Rule.parse(part, workflows) for part in rest.split(',')]
        return cls(name, rules, workflows)

    def simplify(self):
        while (
            len(self.rules) > 1
            and self.rules[-2].destination == self.rules[-1].destination
        ):
            del self.rules[-2]
        if len(self.rules) == 1:
            [remaining_rule] = self.rules
            assert remaining_rule.condition is None
            for name, wf in self.workflows.items():
                wf.replace_destination(self.name, remaining_rule.destination)

    def replace_destination(self, src, dst):
        changed = False
        for rule in self.rules:
            if rule.destination == src:
                rule.destination = dst
                changed = True
        if changed:
            self.simplify()

    def classify_part(self, part):
        for rule in self.rules:
            if rule.evaluate(part):
                return rule.destination.classify_part(part)

    #@pysnooper.snoop()
    def sum_accepted_ranges(self, ranges):
        total = 0
        for rule in self.rules:
            matched, ranges = rule.split_ranges(ranges)
            if matched:
                total += rule.destination.sum_accepted_ranges(matched)
            if not ranges:
                break
        return total

    def is_valid(self):
        return len(self.rules) > 1 or self.name == 'in'

@dataclasses.dataclass
class FinalWorkflow:
    accept: bool

    def simplify(self):
        return self

    def replace_destination(self, s, d):
        return self

    def is_valid(self):
        return True

    def classify_part(self, part):
        return self.accept

    #@pysnooper.snoop()
    def sum_accepted_ranges(self, ranges):
        if self.accept:
            return math.prod(len(r) for r in ranges.values())
        return 0

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

workflows = {'A': FinalWorkflow(True), 'R': FinalWorkflow(False)}
for line in it:
    if not line:
        break
    wf = Workflow.parse(line, workflows)
    workflows[wf.name] = wf
parts = []
for line in it:
    parts.append(Part.parse(line))
#pprint(parts)

for wf in workflows.values():
    wf.simplify()
print(len(workflows))
pprint(workflows)
workflows = {name: wf for name, wf in workflows.items() if wf.is_valid()}
pprint(workflows)
print(len(workflows))

total = 0
in_wf = workflows['in']
for part in parts:
    result = in_wf.classify_part(part)
    print(part, result)
    if result:
        total += sum(part.categories.values())

print('*** part 1:', total)

in_wf = workflows['in']
result = in_wf.sum_accepted_ranges(dict.fromkeys('xmas', range(1, 4000+1)))

print('*** part 2:', result)
