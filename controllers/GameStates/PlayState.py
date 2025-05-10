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

    def create_overlay_surfaces(self):
        self.board_surface = pygame.Surface((self.engine.width, self.engine.height), pygame.SRCALPHA)
   
    def on_enter(self):
        self.engine.room_renderer.reset_to_orbit_mode()
        self.transition.start()
        self.engine.gomoku_board.clear_board()
        self.turn = self.engine.game_logic.get_current_player()
        self.valid_moves = self.engine.game_logic.get_valid_moves()
        self.engine.room_renderer.set_camera_mode("game")
        print("Entering play state, board cleared")
        
        # Reset the 3D mode flag
        self.in_3d_mode = True
        
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.engine.running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.engine.change_state(self.engine.menu_state)
            
            self.engine.game_logic.run(events,self.engine.room_renderer.gomoku_board,self.engine.width,self.engine.height)

    def update(self, dt):
        self.transition.update(on_midpoint=lambda: self.switch_to_2d_mode())
        
    def switch_to_2d_mode(self):
        self.in_3d_mode = False
        
    def render(self):
        if self.in_3d_mode:
            self.engine.room_renderer.draw()
        else:
            
            glClearColor(0.780, 0.643, 0.463, 1.0)
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            glMatrixMode(GL_PROJECTION)
            glPushMatrix()
            glLoadIdentity()
            glOrtho(0, self.engine.width, self.engine.height, 0, -1, 1)
            
            glMatrixMode(GL_MODELVIEW)
            glPushMatrix()
            glLoadIdentity()
            
            self.engine.room_renderer.gomoku_board.draw_2D(self.board_surface,self.turn,self.valid_moves)
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