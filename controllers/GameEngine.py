import pygame
import sys
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from models.room import RoomRenderer
# from controllers.BoardRenderer2D import BoardRenderer2D

from controllers.GameStates.MenuState import MenuState
from controllers.GameStates.PlayState import PlayState

from models.game import GomokuGame
from models.board import GomokuBoard

class GameEngine:
    def __init__(self, width=1280, height=720, fps=120, dramatic_mode = True):
        pygame.init()
        pygame.display.set_caption('Gomoku')

        self.width = width
        self.height = height
        self.fps = fps
        self.clock = pygame.time.Clock()
        self.running = True
        self.full_screen = False
        self.dramatic_mode = dramatic_mode

        self.gomoku_board = GomokuBoard()
        self.game_logic = GomokuGame(self.gomoku_board)
        if self.dramatic_mode:
            print("3D mode")
            pygame.display.gl_set_attribute(GL_MULTISAMPLEBUFFERS, 1)
            pygame.display.gl_set_attribute(GL_MULTISAMPLESAMPLES, 4)
            self.screen = pygame.display.set_mode((self.width, self.height), pygame.OPENGL | pygame.DOUBLEBUF | pygame.RESIZABLE)
            glClearColor(0.1, 0.1, 0.1, 1.0)
            glEnable(GL_DEPTH_TEST)
            self.room_renderer = RoomRenderer(self.gomoku_board)

            self.menu_state = MenuState(self)
            self.play_state = PlayState(self)
            self.current_state = self.menu_state
            self.resize(width, height)



    def change_state(self, new_state):
        if self.current_state:
            self.current_state.on_exit()
            
        # Handle camera transition when switching to play state
        if new_state == self.play_state:
            self.room_renderer.set_camera_mode("game")
            self.room_renderer.start_camera_transition()
        elif new_state == self.menu_state:
            self.room_renderer.set_camera_mode("orbit")
            self.room_renderer.start_camera_transition()
            
        self.current_state = new_state
        self.current_state.on_enter()
    
    def resize(self, width, height):
        if height == 0:
            height = 1
        
        self.width = width
        self.height = height
        
        if hasattr(self.current_state, 'create_overlay_surfaces'):
            self.current_state.create_overlay_surfaces()
        
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, (width / height), 0.1, 200.0)
        glMatrixMode(GL_MODELVIEW)

    def handle_events(self):
        events = pygame.event.get()
        
        for event in events:
            if event.type == VIDEORESIZE:
                if not self.full_screen:
                    self.width, self.height = event.size
                    self.screen = pygame.display.set_mode((self.width, self.height), pygame.OPENGL | pygame.DOUBLEBUF | pygame.RESIZABLE)
                    self.resize(self.width, self.height)
            elif event.type == KEYDOWN:
                if event.key == K_f:
                    self.full_screen = not self.full_screen
                    if self.full_screen:
                        modes = pygame.display.list_modes()
                        self.screen = pygame.display.set_mode(modes[0], pygame.FULLSCREEN | pygame.OPENGL)
                        self.resize(modes[0][0], modes[0][1])
                    else:
                        self.screen = pygame.display.set_mode((self.width, self.height), pygame.OPENGL | pygame.DOUBLEBUF | pygame.RESIZABLE)
                        self.resize(self.width, self.height)
        
        self.current_state.handle_events(events)

    def run(self):
        if self.dramatic_mode:
            while self.running:
                self.clock.tick(self.fps)
                self.handle_events()
                self.current_state.render()
                self.current_state.update(1)
                pygame.display.flip()
        else:
            self.game_logic.run_debug()
        pygame.quit()
        sys.exit()