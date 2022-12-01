import numpy

with open('data.txt') as file:
    numbers = [int(s) for s in file.readline().split(',')]
    boards = []
    for line in file:
        if not line.strip():
            boards.append([])
        else:
            boards[-1].append([int(s) for s in line.split()])
boards = numpy.array(boards)

print(numbers)
print(boards)

done_template = numpy.zeros(boards.shape[0], dtype=int)

def solve(part1=True):
    marks = boards * 0
    for called_number in numbers:
        marks[boards == called_number] = 1
        done_boards = done_template.copy()
        for axis in 1, 2:
            done_boards[marks.all(axis=axis).any(axis=1)] = 1
        if part1:
            if done_boards.any():
                winning_board_no = done_boards.argmax()
                break
        else:
            if done_boards.all():
                winning_board_no = prev_done_boards.argmin()
                break
        prev_done_boards = done_boards
    winning_board = boards[winning_board_no]
    winning_marks = marks[winning_board_no]
    print(winning_board_no)
    return winning_board[winning_marks == 0].sum() * called_number
print('Part 1:', solve())
print('Part 2:', solve(False))
