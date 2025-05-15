import random
import pygame
from controllers.minmax import minmax
from controllers.alpha_beta import alpha_beta
from models.utils import check_game_status
import time

class GomokuGame:
    def __init__(self, board):
        self.board = board
        self.current_player = 1
        self.winner = None
        self.game_over = False
        self.game_mode = False  # False = Player vs AI, True = AI vs AI
        self.last_ai_move_time = 0

    def reset(self):
        self.current_player = 1
        self.winner = None
        self.game_over = False
        self.board.clear_board()

    def place_stone(self, row, col):
        if self.game_over:
            return False

        if self.board.place_stone(row, col, self.current_player):
            if self.check_win():
                self.winner = self.current_player
                self.game_over = True
            elif self.check_draw():
                self.game_over = True
            else:
                self.current_player = 2 if self.current_player == 1 else 1
            return True
        return False

    def check_win(self):
        game_status = check_game_status(self.board.board_state)
        if(game_status == 2 or game_status == -2):
            return True
        
        return False
    
    def check_draw(self):
        game_status = check_game_status(self.board.board_state)
        if game_status == 0:
            return True
        return False

    def get_valid_moves(self):
        moves = []
        for r in range(self.board.board_size):
            for c in range(self.board.board_size):
                if self.board.board_state[r][c] == 0:
                    moves.append((r, c))
        return moves

    def get_current_player(self):
        return self.current_player
        
    def change_mode(self, mode):
        self.game_mode = mode
        print(f"Game mode changed to {'AI vs AI' if mode else 'Player vs AI'}")

    def print_board(self):
        symbols = {
            0: '-', 
            1: '●',
            2: '○'
        }

        print("   ", end="")  
        for c in range(self.board.board_size):
            print(f"{c:2}", end=" ")
        print()

        for r in range(self.board.board_size):
            print(f"{r:2} ", end="") 
            for c in range(self.board.board_size):
                print(f"{symbols[self.board.board_state[r][c]]} ", end="")
            print()
        print("\n")

    def ai_move(self, op):
        # If game is already over, don't attempt to make a move
        if self.game_over:
            return None
            
        valid_moves = self.get_valid_moves()
        if not valid_moves:
            return None
            
        if (op == "MinMax"):
            best_move = minmax(self.board, valid_moves, self.current_player)
        elif (op == "AlphaBeta"):
            best_move = alpha_beta(self.board, valid_moves, self.current_player)
            # best_move = minmax(self.board, valid_moves, self.current_player)

        return best_move
    
    def run(self, events, board, width, height):
        if self.game_over:
            return

        cell_size = board.cell_size
        cell_size = min(width, height) // (board.board_size * 1.2)
        offset_x = board.offset_x
        offset_y = board.offset_y
        hint_radius = cell_size // 3
        
        # Player vs AI mode
        if self.game_mode == False:
            if self.current_player == 1:  # Human player's turn
                for event in events:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        valid_moves = self.get_valid_moves()
                        for row, col in valid_moves:
                            if board.is_hovering_cell(mouse_pos, row, col, offset_x, offset_y, cell_size, hint_radius):
                                if not self.place_stone(row, col):
                                    print("Invalid move. Try again.")
                                    return
                                print(f"Player 1 placed a stone at ({row}, {col})")
                                break
            else:  # AI's turn
                print(f"Player 2's turn (AI)")
                move = self.ai_move("AlphaBeta")
                if move is None:
                    return
                    
                row, col = move
                if row is not None and col is not None:
                    print(f"AI chose: {row} {col}")
                    if not self.place_stone(row, col):
                        return
                    print(f"AI placed a stone at ({row}, {col})")
        
        # AI vs AI is handled in PlayState

        if self.game_over:
            if self.winner:
                print(f"Player {self.winner} wins!")
            else:
                print("Draw!")

    def run_debug(self):
        self.board.clear_board()
        while not self.game_over:
            self.print_board()

            if self.current_player == 1:
                print(f"Player {self.get_current_player()}'s turn!")
                print("Enter your move as row col (0-based indexing): ")
                try:
                    row, col = map(int, input().split())
                    if not (0 <= row < self.board.board_size and 0 <= col < self.board.board_size):
                        print("Invalid move. Try again.")
                        continue

                    if not self.place_stone(row, col):
                        print("Invalid move. Try again.")
                    elif self.game_over:
                        self.print_board()
                        if self.winner:
                            print(f"Player {self.winner} wins!")
                        else:
                            print("Draw!")
                        break
                except ValueError:
                    print("Invalid input! Please enter two integers separated by a space.")
            else:
                print(f"Player {self.get_current_player()}'s turn (AI)!")
                move = self.ai_move("AlphaBeta")
                if move is None:
                    continue
                    
                row, col = move
                if row is not None and col is not None:
                    print(f"AI chose: {row} {col}")
                    if not self.place_stone(row, col):
                        continue
                    elif self.game_over:
                        self.print_board()
                        if self.winner:
                            print(f"Player {self.winner} wins!")
                        else:
                            print("Draw!")
                        break