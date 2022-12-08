import sys
import numpy
import itertools

data = sys.stdin.read().splitlines()

trees = numpy.array([[int(c) for c in r] for r in data], dtype=int)
print(trees)
visible = numpy.zeros(trees.shape, dtype=int)
paths = []
# Generate a list of paths -- lists of (row, col) coordinates -- to walk
for r, row in enumerate(trees):
    paths.append(list(zip(itertools.repeat(r), range(len(row)))))
    paths.append(list(zip(itertools.repeat(r), range(len(row)-1, -1, -1))))
for c, col in enumerate(trees.T):
    paths.append(list(zip(range(len(col)), itertools.repeat(c))))
    paths.append(list(zip(range(len(col)-1, -1, -1), itertools.repeat(c))))
print(paths)
# Walk down each path, marking visible trees
for path in paths:
    max_size = -1
    for r, c in path:
        is_tall = trees[r, c] > max_size
        print(f"{r=}, {c=} ({trees[r, c]} > {max_size}) {is_tall}")
        if is_tall:
            visible[r, c] = 1
            max_size = trees[r, c]
print(visible)

print('*** part 1:', visible.sum())

scenic_scores = numpy.ones(trees.shape, dtype=int)
for r, tree_row in enumerate(trees):
    for c, tree in enumerate(tree_row):
        # Generate a list of paths
        paths = [
            list(zip(itertools.repeat(r), range(c+1, len(trees)))),
            list(zip(itertools.repeat(r), range(c-1, -1, -1))),
            list(zip(range(r+1, len(trees[0])), itertools.repeat(c))),
            list(zip(range(r-1, -1, -1), itertools.repeat(c))),
        ]
        # Walk down each path, until a tree is too big
        for path in paths:
            score = 0
            for pr, pc in path:
                score += 1
                print(f"{pr=} {pc=} {score}")
                if trees[pr, pc] >= tree:
                    break
            scenic_scores[r, c] *= score

print(scenic_scores)


print('*** part 2:', scenic_scores.max())
