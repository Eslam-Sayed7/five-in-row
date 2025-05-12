import sys
from models.utils import check_game_status, calculate_best_depth


def get_best_move(board, depth, player, first_time=True):
    # Return a move (x, y): [0, 14]
    board_state = board.board_state
    board_size = board.board_size


    status_num = check_game_status(board_state)


    if (status_num != 1 or depth == 0):
        return status_num

    min_score = sys.maxsize
    max_score = -sys.maxsize - 1
    final_i, final_j = -1, -1

    for i in range(board_size):
        for j in range(board_size):
            if board_state[i][j] == 0:
                if player == 1:  # '●'s turn
                    board_state[i][j] = 1 # set the cell to '●'
                    score = get_best_move(board, depth - 1, 2, False)
                    board_state[i][j] = 0
                    if max_score < score:
                        max_score = score
                        final_i, final_j = i, j

                elif player == 2:  # '○'s turn
                    board_state[i][j] = 2 # set the cell to '○'
                    score = get_best_move(board, depth - 1, 1, False)
                    board_state[i][j] = 0
                    if min_score > score:
                        min_score = score
                        final_i, final_j = i, j

    if first_time:
        return final_i, final_j

    return max_score if player == 1 else min_score


def minmax(board, valid_moves, player):
    depth = calculate_best_depth(valid_moves)
    print(f"Depth: {depth}")
    best_move = get_best_move(board, depth, player)
    return best_move
