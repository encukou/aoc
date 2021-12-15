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

marks = boards * 0
for called_number in numbers:
    marks[boards == called_number] = 1
    print(marks)
    for axis in 1, 2:
        done_boards = marks.all(axis=axis).any(axis=1)
        if done_boards.any():
            winning_board_no = done_boards.argmax()
            break
    else:
        continue
    break
winning_board = boards[winning_board_no]
winning_marks = marks[winning_board_no]
print('Part 1:', winning_board[winning_marks == 0].sum() * called_number)
