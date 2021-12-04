input = open("/Users/cesar/04/input.txt", "r").readlines()

nums = input[0].split(",")

boards = []
board = []

winners = []

for l in input[1:]:
    if l.strip() != "":
        board.append(l.strip().split())
    else:
        if board:
            boards.append(board)
            winners.append(False)
            board = []

boards.append(board)
winners.append(False)


def check_board(b):
    for row in b:
        all_row = True
        for c in row:
            if c != "X":
                all_row = False
        if all_row:
            return True

    for i in range(len(b[0])):
        all_col = True
        for row in b:
            if row[i] != "X":
                all_col = False
        if all_col:
            return True


def check_boards(boards, winners):
    winner = None
    for idx, b in enumerate(boards):
        if not winners[idx]:
            if check_board(b):
                winners[idx] = True
                winner = b

    return winner


def sum_unmarked(board):
    sum = 0
    for row in board:
        for c in row:
            if c != "X":
                sum += int(c)

    return sum


winnernum = 0
for n in nums:
    for b in boards:
        for ridx, row in enumerate(b):
            for cidx, c in enumerate(row):
                if c == n:
                    # match
                    b[ridx][cidx] = "X"

    winner = check_boards(boards, winners)
    if winner:
        winnernum += 1
        print(f"WINNER {winnernum}")
        print(sum_unmarked(winner) * int(n))
