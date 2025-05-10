from OpenGL.GL import *
from OpenGL.GLU import *
import math
import time
from models.board import *
from controllers.ObjLoader import *

class RoomRenderer:
    def __init__(self,board):
        self.start_time = time.time()
        self.orbit_radius = 10.0      
        self.orbit_height = 10.0      
        self.vertical_amplitude = 1.0
        self.orbit_speed = 0.15      
        self.vertical_speed = 0.3    
        self.tile_size = 10.0 
        self.room_size = 50.0
        self.gomoku_board = board
        self.camera_mode = "orbit"
        self.previous_camera_mode = "orbit"
        
        self.transitioning = False
        self.transition_start_time = 0
        self.transition_duration = 1.5
        
        # Camera position variables
        self.current_cam_x = 0
        self.current_cam_y = 0
        self.current_cam_z = 0
        self.current_target_x = 0
        self.current_target_y = 0
        self.current_target_z = 0
        self.models = {}
        try:
            self.models['table'] = ObjLoader.load_obj(self.models,'assets/table.obj', name = 'table')
            self.models['chair'] = ObjLoader.load_obj(self.models,'assets/chair.obj', name = 'chair')
            if self.models['table'] is None or self.models['chair'] is None:
                print("Model failed to load.")
        except Exception as e:
            print(f"Exception while loading table model: {e}")
            self.models['table'] = None
            self.models['chair'] = None


    def set_camera_mode(self, mode):
        if mode in ["orbit", "game"]:
            if mode != self.camera_mode:
                self.previous_camera_mode = self.camera_mode
                self.camera_mode = mode
                self.start_camera_transition() 
                print(f"Camera mode changed to: {mode}")
        else:
            print(f"Invalid camera mode: {mode}")

    def reset_to_orbit_mode(self):
        self.camera_mode = "orbit"
        self.previous_camera_mode = "orbit"
        self.transitioning = False

    def start_camera_transition(self):
        self.transitioning = True
        self.transition_start_time = time.time()
        self.start_cam_x, self.start_cam_y, self.start_cam_z, self.start_target_x, self.start_target_y, self.start_target_z = self.get_raw_camera_position(self.previous_camera_mode)
        self.end_cam_x, self.end_cam_y, self.end_cam_z, self.end_target_x, self.end_target_y, self.end_target_z = self.get_raw_camera_position(self.camera_mode)
        
    def get_raw_camera_position(self, mode):
        if mode == "orbit":
            elapsed_time = time.time() - self.start_time
            angle = elapsed_time * self.orbit_speed
            x = self.orbit_radius * math.sin(angle)
            z = self.orbit_radius * math.cos(angle)
            y = self.orbit_height + self.vertical_amplitude * math.sin(elapsed_time * self.vertical_speed)
            return x, y, z, 0, 4, 0
        elif mode == "game":
            return 0, 15, 0.00001, 0, 0, 0 

    def get_camera_position(self):
        if self.transitioning:
            elapsed = time.time() - self.transition_start_time
            progress = min(elapsed / self.transition_duration, 1.0)
            
            progress = 0.5 - 0.5 * math.cos(progress * math.pi)
            cam_x = self.start_cam_x + (self.end_cam_x - self.start_cam_x) * progress
            cam_y = self.start_cam_y + (self.end_cam_y - self.start_cam_y) * progress
            cam_z = self.start_cam_z + (self.end_cam_z - self.start_cam_z) * progress
            target_x = self.start_target_x + (self.end_target_x - self.start_target_x) * progress
            target_y = self.start_target_y + (self.end_target_y - self.start_target_y) * progress
            target_z = self.start_target_z + (self.end_target_z - self.start_target_z) * progress
            if progress >= 1.0:
                self.transitioning = False
                
            return cam_x, cam_y, cam_z, target_x, target_y, target_z
        else:
            return self.get_raw_camera_position(self.camera_mode)

    def draw_floor_tile(self, x, z, is_light):
        self.light_tile_color = (0.9, 0.9, 0.9) 
        self.dark_tile_color = (0.8, 0.8, 0.8)
        if is_light:
            glColor3fv(self.light_tile_color)
        else:
            glColor3fv(self.dark_tile_color)
        
        glBegin(GL_QUADS)
        glVertex3f(x, 0, z)
        glVertex3f(x + self.tile_size, 0, z)
        glVertex3f(x + self.tile_size, 0, z + self.tile_size)
        glVertex3f(x, 0, z + self.tile_size)
        glEnd()

    def draw(self, z=None):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        cam_x, cam_y, cam_z, target_x, target_y, target_z = self.get_camera_position()

        gluLookAt(cam_x, cam_y, cam_z,  # Camera position
                  target_x, target_y, target_z,  # Look at point  
                  0, 1, 0)  # Up vector
        
        room_alpha = 1.0
        if self.camera_mode == "game" and not self.transitioning:
            room_alpha = 0.0 

        if room_alpha > 0:
            for x in range(-int(self.room_size), int(self.room_size), int(self.tile_size)):
                for z in range(-int(self.room_size), int(self.room_size), int(self.tile_size)):
                    is_light = ((int(x / self.tile_size) + int(z / self.tile_size)) % 2) == 0
                    self.draw_floor_tile(x, z, is_light)

            # Ceiling
            glBegin(GL_QUADS)
            glColor3f(0.9, 0.9, 0.9)
            glVertex3f(-self.room_size, self.room_size, -self.room_size)
            glVertex3f(self.room_size, self.room_size, -self.room_size)
            glVertex3f(self.room_size, self.room_size, self.room_size)
            glVertex3f(-self.room_size, self.room_size, self.room_size)
            glEnd()

            # Back wall
            glBegin(GL_QUADS)
            glColor3f(0.8, 0.8, 0.8)
            glVertex3f(-self.room_size, 0, -self.room_size)
            glVertex3f(self.room_size, 0, -self.room_size)
            glVertex3f(self.room_size, self.room_size, -self.room_size)
            glVertex3f(-self.room_size, self.room_size, -self.room_size)
            glEnd()

            # Front wall
            glBegin(GL_QUADS)
            glColor3f(0.8, 0.8, 0.8)
            glVertex3f(-self.room_size, 0, self.room_size)
            glVertex3f(self.room_size, 0, self.room_size)
            glVertex3f(self.room_size, self.room_size, self.room_size)
            glVertex3f(-self.room_size, self.room_size, self.room_size)
            glEnd()

            # Left wall
            glBegin(GL_QUADS)
            glColor3f(0.85, 0.85, 0.85)
            glVertex3f(-self.room_size, 0, -self.room_size)
            glVertex3f(-self.room_size, 0, self.room_size)
            glVertex3f(-self.room_size, self.room_size, self.room_size)
            glVertex3f(-self.room_size, self.room_size, -self.room_size)
            glEnd()

            # Right wall
            glBegin(GL_QUADS)
            glColor3f(0.85, 0.85, 0.85)
            glVertex3f(self.room_size, 0, -self.room_size)
            glVertex3f(self.room_size, 0, self.room_size)
            glVertex3f(self.room_size, self.room_size, self.room_size)
            glVertex3f(self.room_size, self.room_size, -self.room_size)
            glEnd()

            ObjLoader.draw_obj(self.models['table'], position=(0, 0, 0), rotation=(-90,1,0,0), scale=(0.1,0.1,0.1))
            ObjLoader.draw_obj(self.models['chair'], position=(0, 3, -8), rotation=(-90,1,0,0), scale=(0.07,0.07,0.07))
            glPushMatrix()
            glRotatef(180, 0, 1, 0)
            ObjLoader.draw_obj(self.models['chair'], position=(0, 3, -8), rotation=(-90,1,0,0), scale=(0.07,0.07,0.07))
            glPopMatrix()
        
        if self.camera_mode == "game" and not self.transitioning:
            self.gomoku_board.clear_board()
            glClearColor(0.780, 0.643, 0.463, 1.0)
        else:
            glPushMatrix()
            glTranslatef(0, 4.7, 0)
            glScalef(0.4, 0.4, 0.4)
            self.gomoku_board.draw_3D()
            glPopMatrix()