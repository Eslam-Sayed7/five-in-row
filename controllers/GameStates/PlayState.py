
import pygame
from controllers.TransitionManager import TransitionManager
from controllers.GameStates.GameState import GameState
from OpenGL.GL import *

class PlayState(GameState):
    def __init__(self, engine):
        super().__init__(engine)
        self.transition = TransitionManager(engine.width, engine.height)
        self.create_overlay_surfaces()
        self.in_3d_mode = True
        self.turn = 1
        self.valid_moves = None
        self.game_mode = engine.game_mode
        self.last_ai_move_time = 0
        self.ai_move_delay = 3000 
        self.winner = None
    def create_overlay_surfaces(self):
        self.board_surface = pygame.Surface((self.engine.width, self.engine.height), pygame.SRCALPHA)
        
    def on_enter(self):
        self.engine.room_renderer.reset_to_orbit_mode()
        self.transition.start()
        self.engine.gomoku_board.clear_board()
        self.turn = self.engine.game_logic.get_current_player()
        self.valid_moves = self.engine.game_logic.get_valid_moves()
        self.engine.room_renderer.set_camera_mode("game")
        self.game_mode = self.engine.game_mode
        print("Entering play state, board cleared")
        self.engine.game_logic.reset()
        self.winner = None
        self.engine.game_logic.change_mode(self.game_mode)
        self.in_3d_mode = True
        self.last_ai_move_time = pygame.time.get_ticks()
        
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.engine.running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.engine.change_state(self.engine.menu_state)
        
        self.process_game_logic(events)
        
    def process_game_logic(self, events):
        # For human vs AI mode
        if not self.game_mode:
            self.engine.game_logic.run(events, self.engine.gomoku_board, 
                                      self.engine.width, self.engine.height)
            self.turn = self.engine.game_logic.get_current_player()
            self.winner = self.engine.game_logic.winner

        # For AI vs AI mode
        else:
            if self.engine.game_logic.game_over:
                if self.engine.game_logic.winner:
                    winner_name = "MinMax AI" if self.engine.game_logic.winner == 1 else "Alpha-Beta AI"
                    print(f"{winner_name} wins!")
                    self.winner = self.engine.game_logic.winner
                else:
                    print("Draw!")
                    self.winner = "Draw"
                return
                
                
            current_time = pygame.time.get_ticks()
            if current_time - self.last_ai_move_time > self.ai_move_delay:
                self.last_ai_move_time = current_time
                
                current_player = self.engine.game_logic.get_current_player()
                if current_player == 1:
                    algorithm = "MinMax"
                    ai_name = "MinMax AI"
                else:
                    algorithm = "AlphaBeta"
                    ai_name = "Alpha-Beta AI"
                
                print(f"AI ({algorithm}) Turn: ")
                result = self.engine.game_logic.ai_move(algorithm)
                
                if result is None or isinstance(result, int):
                    print(f"Error: AI move returned invalid result: {result}")
                    return
                    
                row, col = result
                print(f"AI ({algorithm}) chose: {row} {col}")
                
                if self.engine.game_logic.place_stone(row, col):
                    print(f"{ai_name} placed a stone at ({row}, {col})")
                    
                self.turn = self.engine.game_logic.get_current_player()
                self.valid_moves = self.engine.game_logic.get_valid_moves()
                
                if self.engine.game_logic.game_over:
                    if self.engine.game_logic.winner:
                        winner_name = "MinMax AI" if self.engine.game_logic.winner == 1 else "Alpha-Beta AI"
                        print(f"{winner_name} wins!")
                        self.winner = self.engine.game_logic.winner
                    else:
                        print("Draw!")
                        self.winner = "Draw"

    def update(self, dt):
        self.transition.update(on_midpoint=lambda: self.switch_to_2d_mode())
        
    def switch_to_2d_mode(self):
        self.in_3d_mode = False
        
    def render(self):
        if self.in_3d_mode:
            self.engine.room_renderer.draw()
        else:
            # 2D rendering mode
            glClearColor(0.780, 0.643, 0.463, 1.0)
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glMatrixMode(GL_PROJECTION)
            glPushMatrix()
            glLoadIdentity()
            glOrtho(0, self.engine.width, self.engine.height, 0, -1, 1)
            
            glMatrixMode(GL_MODELVIEW)
            glPushMatrix()
            glLoadIdentity()
            
            self.engine.room_renderer.gomoku_board.draw_2D(self.board_surface, self.turn, self.valid_moves,self.winner)
            board_texture = pygame.image.tostring(self.board_surface, "RGBA", True)
            
            glEnable(GL_BLEND)
            glWindowPos2d(0, 0)
            glDrawPixels(self.engine.width, self.engine.height, GL_RGBA, GL_UNSIGNED_BYTE, board_texture)
            glDisable(GL_BLEND)
            glMatrixMode(GL_PROJECTION)
            glPopMatrix()
            glMatrixMode(GL_MODELVIEW)
            glPopMatrix()
        
        if self.transition:
            self.transition.render()