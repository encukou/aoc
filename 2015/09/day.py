import sys
import itertools

data = sys.stdin.read().strip().splitlines()

example = """
London to Dublin = 464
London to Belfast = 518
Dublin to Belfast = 141
""".strip().splitlines()

def find_best(lines, func=min):
    cities = set()
    distances = {}
    for line in lines:
        match line.split():
            case a, 'to', b, '=', dist:
                distances[a, b] = distances[b, a] = int(dist)
                cities.update((a, b))
            case _:
                raise ValueError(line)
    cities = sorted(cities)
    def distance(route):
        return sum(distances[a, b] for a, b in zip(route, route[1:]))
    return func(
        (distance(route), route)
        for route in itertools.permutations(cities)
    )[0]

print(find_best(example))
print(f'*** part 1:', find_best(data))
print(f'*** part 2:', find_best(data, max))
