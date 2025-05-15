import pygame
import sys
from pygame.locals import *

class Button:
    def __init__(self, text, position, font, width=200, height=40, state="Main", text_color = (220,200,200),hover_color = (155, 155, 155)):
        self.text = text
        self.position = position
        self.font = font
        self.width = width
        self.height = height
        self.text_color = text_color
        self.hover_color = hover_color
        self.hover = False
        self.state = state
    def is_hovered(self, mouse_pos, offset_x):
        adjusted_x = mouse_pos[0] - offset_x
        return (self.position[0] <= adjusted_x <= self.position[0] + self.width and
                self.position[1] <= mouse_pos[1] <= self.position[1] + self.height)
        
    def draw(self, surface):
        button_rect = pygame.Rect(self.position[0], self.position[1], self.width, self.height)

        current_text_color = (155, 155, 155) if self.hover else self.text_color
        text_surface = self.font.render(self.text, True, current_text_color)
        text_rect = text_surface.get_rect(midleft=(button_rect.left + 10, button_rect.centery))
        surface.blit(text_surface, text_rect)

class ArrowButton(Button):
    def __init__(self, text, position, font, width=200, height=40, min_value=5, max_value=15, state="Main"):
        super().__init__(text, position, font, width, height)
        self.value = min_value
        self.min_value = min_value
        self.max_value = max_value
        self.state = state
    def update_value(self):
        if self.value < self.max_value:
            self.value += 1
        else:
            self.value = self.min_value

    def draw(self, surface):
        button_rect = pygame.Rect(self.position[0], self.position[1], self.width, self.height)
        current_text_color = self.hover_color if self.hover else self.text_color
        text_surface = self.font.render(f"{self.text}: {self.value} x {self.value}", True, current_text_color)
        text_rect = text_surface.get_rect(midleft=(button_rect.left + 10, button_rect.centery))
        surface.blit(text_surface, text_rect)


class ToggleButton(Button):
    def __init__(self, text, position, font, width=200, height=40, state="Main"):
        super().__init__(text, position, font, width, height,state)
        self.value = False
        self.text = "Player vs AI"
    def update_value(self):
        self.value = not self.value
    def draw(self, surface):
        button_rect = pygame.Rect(self.position[0], self.position[1], self.width, self.height)
        current_text_color = (155, 155, 155) if self.hover else self.text_color
        if (self.value == True):
            self.text = "AI vs AI" # 1
        else:
            self.text = "Player vs AI" # 0

        text_surface = self.font.render(f"Mode: {self.text}" , True, current_text_color)
        text_rect = text_surface.get_rect(midleft=(button_rect.left + 10, button_rect.centery))
        surface.blit(text_surface, text_rect)