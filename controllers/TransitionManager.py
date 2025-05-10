from time import time
import pygame
from OpenGL.GL import *

class TransitionManager:
    def __init__(self, width, height, duration=1.5, pause_duration=1.0):
        self.width = width
        self.height = height
        self.transition_duration = duration
        self.transition_pause_duration = pause_duration
        self.transition_start_time = 0
        self.transitioning = False
        self.fade_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        self.state_switched = False

    def start(self):
        self.transitioning = True
        self.transition_start_time = time()
        self.state_switched = False

    def update(self, on_midpoint=None):
        if not self.transitioning:
            return

        elapsed = time() - self.transition_start_time
        midpoint = self.transition_duration / 2
        pause_end = midpoint + self.transition_pause_duration

        if elapsed >= midpoint and not self.state_switched:
            if on_midpoint:
                on_midpoint()
            self.state_switched = True

        if elapsed > pause_end + (self.transition_duration / 2):
            self.transitioning = False

    def render(self):
        if not self.transitioning:
            return

        elapsed = time() - self.transition_start_time
        midpoint = self.transition_duration / 2
        pause_end = midpoint + self.transition_pause_duration
        fade_out_duration = midpoint
        fade_in_duration = midpoint

        if elapsed < fade_out_duration:
            fade_percent = elapsed / fade_out_duration
            alpha = int(fade_percent * 255)
        elif elapsed < pause_end:
            alpha = 255
        else:
            fade_in_elapsed = elapsed - pause_end
            fade_percent = 1.0 - (fade_in_elapsed / fade_in_duration)
            alpha = int(fade_percent * 255)

        if alpha > 0:
            self.fade_surface.fill((0, 0, 0, alpha))
            fade_texture = pygame.image.tostring(self.fade_surface, "RGBA", True)

            glMatrixMode(GL_PROJECTION)
            glPushMatrix()
            glLoadIdentity()
            glOrtho(0, self.width, self.height, 0, -1, 1)
            glMatrixMode(GL_MODELVIEW)
            glPushMatrix()
            glLoadIdentity()

            glEnable(GL_BLEND)
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
            glWindowPos2d(0, 0)
            glDrawPixels(self.width, self.height, GL_RGBA, GL_UNSIGNED_BYTE, fade_texture)
            glDisable(GL_BLEND)

            glMatrixMode(GL_PROJECTION)
            glPopMatrix()
            glMatrixMode(GL_MODELVIEW)
            glPopMatrix()
