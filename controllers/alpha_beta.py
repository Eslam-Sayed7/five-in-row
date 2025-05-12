import sys
from models.utils import check_game_status,calculate_best_depth

def get_best_move(board, depth, alpha, beta, player, first_time=True):
    board_state = board.board_state
    board_size = board.board_size

    status_num = check_game_status(board_state)

    if status_num != 1 or depth == 0:
        return status_num

    final_i, final_j = -1, -1

    for i in range(board_size):
        for j in range(board_size):
            if board_state[i][j] == 0:
                if player == 1:  # '●'s turn (maximizing player)
                    board_state[i][j] = 1 # set the cell to '●'
                    score = get_best_move(board, depth - 1, alpha, beta, 2, False)
                    board_state[i][j] = 0
                    
                    if score > alpha:
                        alpha = score
                        final_i, final_j = i, j

                    if alpha >= beta:
                        break
                
                elif player == 2:  # '○'s turn (minimizing player)
                    board_state[i][j] = 2
                    score = get_best_move(board, depth - 1, alpha, beta, 1, False)
                    board_state[i][j] = 0
                    
                    if score < beta:
                        beta = score
                        final_i, final_j = i, j
                    
                    if alpha >= beta:
                        break

        if player == 1 and alpha >= beta:
            break
        elif player == 2 and alpha >= beta:
            break

    if first_time:
        return final_i, final_j

    return alpha if player == 1 else beta

def alpha_beta(board, valid_moves, player):
    depth = calculate_best_depth(valid_moves)
    depth += 1
    print(f"Alpha-Beta Depth: {depth}")

    alpha = -sys.maxsize - 1  # Best score for maximizer (player 1)
    beta = sys.maxsize        # Best score for minimizer (player 2)
    
    best_move = get_best_move(board, depth, alpha, beta, player)
    return best_move
