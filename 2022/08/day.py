import sys
import numpy
import itertools

data = sys.stdin.read().splitlines()

trees = numpy.array([[int(c) for c in r] for r in data], dtype=int)
print(trees)
visible = numpy.zeros(trees.shape, dtype=int)
for tree_row, vis_row in itertools.chain(
    zip(trees, visible),
    zip(trees.T, visible.T),
):
    max_size = -1
    for n, tree in enumerate(tree_row):
        if tree > max_size:
            max_size = tree
            vis_row[n] = 1
    max_size = -1
    for n, tree in reversed(list(enumerate(tree_row))):
        if tree > max_size:
            max_size = tree
            vis_row[n] = 1
print(visible)

print('*** part 1:', visible.sum())




print('*** part 2:', ...)
