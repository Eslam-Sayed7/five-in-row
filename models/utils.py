def check_five_in_a_row(line):
    for i in range(len(line) - 4):
        if line[i] != 0 and line[i] == line[i + 1] == line[i + 2] == line[i + 3] == line[i + 4]:
            return line[i]
    return 0


def check_game_status(board):

	# 0  -> Draw
	# 2  -> ● win
	# -2 -> ○ win
	# 1  -> Otherwise

    # Check rows and columns
    for i in range(15):
        row_result = check_five_in_a_row(board[i])
        if row_result != 0:
            return 2 if row_result == 1 else -2

        col_result = check_five_in_a_row([board[j][i] for j in range(15)])
        if col_result != 0:
            return 2 if col_result == 1 else -2

    # Check diagonals
    for i in range(15):
        for j in range(15):
            if i + 4 < 15 and j + 4 < 15:
                if board[i][j] != 0 and board[i][j] == board[i + 1][j + 1] == board[i + 2][j + 2] == board[i + 3][j + 3] == board[i + 4][j + 4]:
                    return 2 if board[i][j] == 1 else -2
            if i + 4 < 15 and j - 4 >= 0:
                if board[i][j] != 0 and board[i][j] == board[i + 1][j - 1] == board[i + 2][j - 2] == board[i + 3][j - 3] == board[i + 4][j - 4]:
                    return 2 if board[i][j] == 1 else -2

    # Check if the game is not finished
    for row in board:
        if 0 in row:
            return 1

    # If no winner and no empty spaces, it's a draw
    return 0