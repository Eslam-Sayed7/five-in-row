from models.button import Button, ArrowButton, ToggleButton
import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from controllers.GameStates.GameState import GameState

class MenuState(GameState):
    def __init__(self, engine):
        super().__init__(engine)
        self.menu_state = "Main"
        self.board_size = 15
        
        font = pygame.font.Font('five-in-row/assets/SupremeSpike-KVO8D.otf', 24)
        self.logo_font = pygame.font.Font('five-in-row/assets/Sanctum-GxmO.ttf', 32)
        self.logo = pygame.Rect(50, 200, 200, 100)
        self.logo_color = (255, 255, 255)
        self.logo_surface = self.logo_font.render("GOMOKU GAME", True, self.logo_color)
        
        button_height, spacing, base_x, base_y = 40, 10, 50, 250
        self.buttons = [
            Button("Start Game", (base_x, base_y), font),
            Button("Settings", (base_x, base_y + (button_height + spacing)), font),
            ArrowButton("Board Size", (base_x, base_y), font, min_value=15, max_value=20, state="Nested"),
            ToggleButton("Mode", (base_x, base_y + 1 * (button_height + spacing)), font, state="Nested"),
            Button("Back", (base_x, base_y + 2 * (button_height + spacing)), font, state="Nested"),
            Button("Quit", (base_x, base_y + 2 * (button_height + spacing)), font),
        ]
        self.create_overlay_surfaces()
    
    def create_overlay_surfaces(self):
        h = self.engine.height
        self.overlay_width = 400
        self.overlay_gradient = pygame.Surface((self.overlay_width, h), pygame.SRCALPHA)
        for x in range(self.overlay_width):
            alpha = int(((self.overlay_width - x) / self.overlay_width) * 255)
            pygame.draw.line(self.overlay_gradient, (0, 0, 0, alpha), (x, 0), (x, h))
        self.overlay_surface = pygame.Surface((self.overlay_width, h), pygame.SRCALPHA)
    
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.engine.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for button in self.buttons:
                    if button.is_hovered(mouse_pos, 0) and button.state == self.menu_state:
                        if button.text == "Start Game":
                            self.engine.change_state(self.engine.play_state)
                        elif button.text == "Settings":
                            self.menu_state = "Nested"
                        elif button.text == "Back":
                            self.menu_state = "Main"
                        elif button.text == "Quit":
                            self.engine.running = False
                        if isinstance(button, ArrowButton) and button.text == "Board Size":
                            button.update_value()
                            self.board_size = button.value
                            self.engine.room_renderer.gomoku_board.set_board_size(self.board_size)
                        elif isinstance(button, ToggleButton):
                            button.update_value()
                        break
    
    def on_enter(self):
        self.create_overlay_surfaces()
    
    def render(self):
        self.engine.room_renderer.draw()
        self.overlay_surface.fill((20, 20, 20, 0))
        
        self.overlay_surface.blit(self.overlay_gradient, (0, 0))
        self.overlay_surface.blit(self.logo_surface, self.logo.topleft)
        
        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            if self.menu_state == button.state:
                button.hover = button.is_hovered(mouse_pos, 0)
                button.draw(self.overlay_surface)
        
        overlay_texture = pygame.image.tostring(self.overlay_surface, "RGBA", True)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glWindowPos2d(0, 0)
        glDrawPixels(self.overlay_width, self.overlay_surface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, overlay_texture)
        glDisable(GL_BLEND)