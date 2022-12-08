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

scenic_scores = numpy.zeros(trees.shape, dtype=int)
for row_n, tree_row in enumerate(trees):
    for col_n, tree in enumerate(tree_row):
        scores = [0] * 4
        for col in range(col_n+1, len(trees)):
            scores[0] += 1
            if trees[row_n, col] >= tree:
                break
        for col in range(col_n-1, -1, -1):
            scores[1] += 1
            if trees[row_n, col] >= tree:
                break
        for row in range(row_n+1, len(trees[0])):
            scores[2] += 1
            if trees[row, col_n] >= tree:
                break
        for row in range(row_n-1, -1, -1):
            scores[3] += 1
            if trees[row, col_n] >= tree:
                break
        score = scores[0]*scores[1]*scores[2]*scores[3]
        print(row_n, col_n, tree, score)
        scenic_scores[row_n, col_n] = score
        
print(scenic_scores)


print('*** part 2:', scenic_scores.max())
