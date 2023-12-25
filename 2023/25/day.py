import sys
import networkx
import math

data = sys.stdin.read().splitlines()
print(data)

graph = networkx.Graph()

for line in data:
    left, rights = line.split(':')
    left = left.strip()
    for right in rights.split():
        graph.add_edge(left, right)
print(graph)

ec = networkx.algorithms.centrality.edge_betweenness_centrality(graph)
for v, e in sorted([(v, e) for e, v in ec.items()])[-3:]:
    print(v, e)
    graph.remove_edge(*e)

components = list(networkx.algorithms.components.connected_components(graph))
print(components)
print(len(components))
assert len(components) == 2


print('*** part 1:', math.prod(len(c) for c in components))
