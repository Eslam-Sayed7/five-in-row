from OpenGL.GL import *
from OpenGL.GLU import *
import math
import time
import pywavefront
from controllers.ObjLoader import *
import pygame
from models.button import *

class GomokuBoard:
    def __init__(self):
        # General Settings
        self.board_size = 15 
        self.cell_size = 1.0  
        self.line_width = 2.0  
        self.margin = 0.5
        self.offset_x = None
        self.offset_y = None
       
        # === 3D settings
        self.board_thickness = 0.5  
        self.stone_radius = 0.4  
        self.stone_height = 0.15 
        self.board_texture = None
        self.board_state = [[0 for _ in range(self.board_size)] for _ in range(self.board_size)]
        self._place_initial_stones()
        # === 2D settings 
        self.background_image_raw = pygame.image.load("assets/textures/background.png")

        self.cell_texture = pygame.image.load("assets/textures/2.jpg")
        self.cell_texture = pygame.transform.scale(self.cell_texture, (self.cell_size, self.cell_size))

        self.font = pygame.font.Font('assets/SupremeSpike-KVO8D.otf', 16)
        self.buttons = [Button("[ESC] Main Menu",(20,20),self.font,50,20,text_color=(0,0,0),hover_color=(0,0,0))]

        self.p1_indicator = pygame.image.load('assets/textures/indicator_p1.png')
        self.p2_indicator = pygame.image.load('assets/textures/indicator_p2.png')

    def clear_board(self):
        self.board_state = [[0 for _ in range(self.board_size)] for _ in range(self.board_size)]

    def _place_initial_stones(self):
        center = self.board_size // 2
        self.board_state[center][center] = 2  
        self.board_state[center][center + 1] = 1 
        self.board_state[center - 1][center] = 1
        self.board_state[center - 1][center + 1] = 2

    def get_board_width(self):
        return self.board_size * self.cell_size
    def get_board_size(self):
        return self.board_size
    def set_board_size(self,new_size):
        self.board_size = new_size
        self.board_state = [[0 for _ in range(self.board_size)] for _ in range(self.board_size)]
        self._place_initial_stones()

    def draw_3D(self):
        self._draw_board_base()
        self._draw_grid_lines()
        self._draw_stones()

    def _draw_board_base(self):
        board_width = self.get_board_width()
        half_width = board_width / 2 + self.margin

        glColor3f(150/255, 113/255, 75/255)
        
        glBegin(GL_QUADS)
        glColor3f(150/255, 113/255, 75/255)
        glVertex3f(-half_width, self.board_thickness, -half_width)
        glVertex3f(half_width, self.board_thickness, -half_width)
        glVertex3f(half_width, self.board_thickness, half_width)
        glVertex3f(-half_width, self.board_thickness, half_width)
        glColor3f(120/255, 83/255, 45/255)
        glVertex3f(-half_width, 0, -half_width)
        glVertex3f(half_width, 0, -half_width)
        glVertex3f(half_width, 0, half_width)
        glVertex3f(-half_width, 0, half_width)
        
        glVertex3f(-half_width, 0, half_width)
        glVertex3f(half_width, 0, half_width)
        glVertex3f(half_width, self.board_thickness, half_width)
        glVertex3f(-half_width, self.board_thickness, half_width)

        glVertex3f(-half_width, 0, -half_width)
        glVertex3f(half_width, 0, -half_width)
        glVertex3f(half_width, self.board_thickness, -half_width)
        glVertex3f(-half_width, self.board_thickness, -half_width)
        
        glVertex3f(-half_width, 0, -half_width)
        glVertex3f(-half_width, 0, half_width)
        glVertex3f(-half_width, self.board_thickness, half_width)
        glVertex3f(-half_width, self.board_thickness, -half_width)
        
        glVertex3f(half_width, 0, -half_width)
        glVertex3f(half_width, 0, half_width)
        glVertex3f(half_width, self.board_thickness, half_width)
        glVertex3f(half_width, self.board_thickness, -half_width)
        glEnd()
        
    def _draw_grid_lines(self):
        board_width = self.get_board_width()
        half_width = board_width / 2
        glColor3f(0.2, 0.1, 0.05)
        glLineWidth(self.line_width)
        
        glBegin(GL_LINES)
        for i in range(self.board_size+1):
            pos = i * self.cell_size - half_width
            glVertex3f(-half_width, self.board_thickness + 0.01, pos)
            glVertex3f(half_width, self.board_thickness + 0.01, pos)
        glEnd()
        
        glBegin(GL_LINES)
        for i in range(self.board_size+1):
            pos = i * self.cell_size - half_width
            glVertex3f(pos, self.board_thickness + 0.01, -half_width)
            glVertex3f(pos, self.board_thickness + 0.01, half_width)
        glEnd()
        
    def _draw_circle(self, x, y, z, radius, slices=12):
        glBegin(GL_TRIANGLE_FAN)
        glVertex3f(x, y, z)
        for i in range(slices + 1):
            angle = 2.0 * math.pi * i / slices
            dx = radius * math.cos(angle)
            dz = radius * math.sin(angle)
            glVertex3f(x + dx, y, z + dz)
        glEnd()
        
    def _draw_stones(self):
        board_width = self.get_board_width()
        half_width = board_width / 2
        
        for row in range(self.board_size):
            for col in range(self.board_size):
                if self.board_state[row][col] == 0:
                    continue
                    
                pos_x = col * self.cell_size - half_width
                pos_z = row * self.cell_size - half_width
                pos_y = self.board_thickness + self.stone_height / 2
                
                if self.board_state[row][col] == 1:
                    glColor3f(0.1, 0.1, 0.1)
                else:
                    glColor3f(0.9, 0.9, 0.9)
                    
                self._draw_stone(pos_x, pos_y, pos_z)
                
    def _draw_stone(self, x, y, z):
        slices = 20
        stacks = 10
        
        quadric = gluNewQuadric()
        glPushMatrix()
        glTranslatef(x, y, z)
        gluSphere(quadric, self.stone_radius, slices, stacks)
        glPopMatrix()
        gluDeleteQuadric(quadric)


    def place_stone(self, row, col, player):
        if self.board_state[row][col] == 0:
            self.board_state[row][col] = player
            return True
        return False

    def draw_2D(self, surface, turn, valid_moves,P1_name,P2_name):
        background_image = self.background_image_raw.convert()
        background_scaled = pygame.transform.scale(background_image, surface.get_size())
        surface.fill((199, 164, 118))
        # surface.blit(background_scaled,(0,0))

        # ==================== Board settings =======================#

        cell_size = min(surface.get_width(), surface.get_height()) // (self.board_size * 1.2)
        
        self.offset_x = (surface.get_width() - cell_size * self.board_size) // 2
        self.offset_y = (surface.get_height() - cell_size * self.board_size) // 2
       
        margin = 40
        margin_color = (150, 113, 75)
        margin_rect = pygame.Rect(self.offset_x - margin//2, self.offset_y - margin//2, 
                                cell_size * self.board_size + margin, 
                                cell_size * self.board_size + margin)

        shadow_color = (100, 75, 50)

        left_offset = 0
        top_offset = 0
        right_offset = 8
        bottom_offset = 8

        top_left_x = self.offset_x - margin//2
        top_left_y = self.offset_y - margin//2
        top_right_x = top_left_x + cell_size * self.board_size + margin
        top_right_y = top_left_y
        bottom_left_x = top_left_x
        bottom_left_y = top_left_y + cell_size * self.board_size + margin
        bottom_right_x = top_right_x
        bottom_right_y = bottom_left_y

        shadow_points = [
            (top_left_x - left_offset, top_left_y - top_offset),  # Top-left
            (top_right_x + right_offset, top_right_y - top_offset),  # Top-right
            (bottom_right_x + right_offset, bottom_right_y + bottom_offset),  # Bottom-right
            (bottom_left_x - left_offset, bottom_left_y + bottom_offset)  # Bottom-left
        ]
        
        # ==================== Board Drawing =======================#

        pygame.draw.polygon(surface, shadow_color, shadow_points)
        pygame.draw.rect(surface, margin_color, margin_rect)

        # Visual trick to look 3D
        pygame.draw.polygon(surface, (199, 164, 118), ((bottom_left_x,bottom_left_y),(shadow_points[3][0],shadow_points[3][1]),(shadow_points[3][0]+5,shadow_points[3][1])))
        pygame.draw.polygon(surface, (199, 164, 118), ((top_right_x,top_right_y),(shadow_points[1][0],shadow_points[1][1]),(shadow_points[1][0],shadow_points[1][1]+10)))
        
        line_color = (41, 30, 22,220)
        # Draw cells
        for row in range(self.board_size):
            for col in range(self.board_size):
                rect = pygame.Rect(
                    self.offset_x + col * cell_size,
                    self.offset_y + row * cell_size,
                    cell_size,
                    cell_size
                )
                pygame.draw.rect(surface, (150, 113, 75), rect)

        # Draw grid lines
        for i in range(self.board_size + 1):
            pygame.draw.line(
                surface, line_color,
                (self.offset_x + i * cell_size, self.offset_y),
                (self.offset_x + i * cell_size, self.offset_y + self.board_size * cell_size),
                2
            )
            pygame.draw.line(
                surface, line_color,
                (self.offset_x, self.offset_y + i * cell_size),
                (self.offset_x + self.board_size * cell_size, self.offset_y + i * cell_size),
                2
                )


        mouse_x, mouse_y = pygame.mouse.get_pos()
        
        for row, col in valid_moves:
            x = self.offset_x + col * cell_size 
            y = self.offset_y + row * cell_size
            hint_radius = cell_size // 3

            circle_surface = pygame.Surface((cell_size, cell_size), pygame.SRCALPHA)

            if self.board_state[row][col] == 0:
                if self.is_hovering_cell((mouse_x, mouse_y), row, col, self.offset_x, self.offset_y, cell_size,hint_radius):
                    if turn == 1:
                        pygame.draw.circle(circle_surface, (50, 50, 50, 50), (cell_size // 2, cell_size // 2), hint_radius)
                    else:
                        pygame.draw.circle(circle_surface, (50, 50, 50, 0), (cell_size // 2, cell_size // 2), hint_radius)
                else:
                    pygame.draw.circle(circle_surface, (50, 50, 50, 0), (cell_size // 2, cell_size // 2), hint_radius)
                surface.blit(circle_surface, (x - cell_size // 2, y - cell_size // 2))

        for row in range(self.board_size):
            for col in range(self.board_size):
                if self.board_state[row][col] == 1 or self.board_state[row][col] == 2:
                    x = self.offset_x + col * cell_size
                    y = self.offset_y + row * cell_size

                    center_x = x 
                    center_y = y 

                    piece_color = (0, 0, 0) if self.board_state[row][col] == 1 else (255, 255, 255)
                    pygame.draw.circle(surface, piece_color, (center_x, center_y), cell_size // 3)
                    self.p1_indicator.set_alpha(20)


        surface.blit(circle_surface, (x - cell_size // 2, y - cell_size // 2))

        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            button.hover = button.is_hovered(mouse_pos, 20)
            button.draw(surface)
        self.p1_indicator = pygame.transform.scale(self.p1_indicator, (150, 150)).convert_alpha()
        surface.blit(self.p1_indicator, (50, (surface.get_height()//2-150)))

        self.p2_indicator = pygame.transform.scale(self.p2_indicator, (150, 150)).convert_alpha()
        surface.blit(self.p2_indicator, (surface.get_width()-200, (surface.get_height()//2-150)))
        self.p1_indicator = pygame.transform.scale(self.p1_indicator, (150, 150)).convert_alpha()
        self.p2_indicator = pygame.transform.scale(self.p2_indicator, (150, 150)).convert_alpha()
        if (turn == 1):
            self.p1_indicator.set_alpha(255)
            self.p2_indicator.set_alpha(20)
        elif (turn == 2):
            self.p2_indicator.set_alpha(255)

        surface.blit(self.p1_indicator, (50, (surface.get_height()//2-150)))
        surface.blit(self.p2_indicator, (surface.get_width()-200, (surface.get_height()//2-150)))

    def is_hovering_cell(self, mouse_pos, row, col, offset_x, offset_y, cell_size, radius):
        mouse_x, mouse_y = mouse_pos
        x = offset_x + col * cell_size
        y = offset_y + row * cell_size
        return (x - radius < mouse_x < x + radius) and (y - radius < mouse_y < y + radius)

    