import pygame
from OpenGL.GL import *

# Función para cargar texturas
def load_texture(image_path):
    texture_surface = pygame.image.load(image_path)
    texture_data = pygame.image.tostring(texture_surface, "RGBA", True)
    width, height = texture_surface.get_size()
    
    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    return texture_id

# Clase para el botón
class Button:
    def __init__(self, x, y, width, height, color, hover_color, texture_path, action=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.hover_color = hover_color
        self.texture_id = load_texture(texture_path)  # Cargar la textura
        self.enabled = True  # Atributo para el estado del botón
        self.action = action

    def draw(self, mx, my):
        if not self.enabled:
            return  # No dibujar el botón si está desactivado

        if self.is_mouse_over(mx, my):
            glColor3f(*self.hover_color)
        else:
            glColor3f(*self.color)

        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 0.0); glVertex2f(self.x, self.y)
        glTexCoord2f(1.0, 0.0); glVertex2f(self.x + self.width, self.y)
        glTexCoord2f(1.0, 1.0); glVertex2f(self.x + self.width, self.y + self.height)
        glTexCoord2f(0.0, 1.0); glVertex2f(self.x, self.y + self.height)
        glEnd()

    def is_mouse_over(self, mx, my):
        return self.x <= mx <= self.x + self.width and self.y <= my <= self.y + self.height

    def check_click(self, mx, my):
        if self.enabled and self.is_mouse_over(mx, my) and self.action:
            self.action()

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False
