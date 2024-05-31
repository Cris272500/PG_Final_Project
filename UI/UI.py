import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

from Options import Credits

# Inicialización de OpenGL
def init_gl(width, height):
    glClearColor(0.0, 0.0, 0.0, 1.0)  # Fondo negro
    glClearDepth(1.0)                 # Configuración de profundidad
    glEnable(GL_DEPTH_TEST)           # Activar la prueba de profundidad
    glDepthFunc(GL_LEQUAL)            # Tipo de prueba de profundidad
    glShadeModel(GL_SMOOTH)           # Sombreado suave
    glEnable(GL_TEXTURE_2D)           # Habilitar texturas
    glEnable(GL_BLEND)                # Habilitar blending para transparencia
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(-1, 1, -1, 1)          # Configuración para vista ortográfica 2D
    glMatrixMode(GL_MODELVIEW)


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
        self.action = action

    def draw(self, mx, my):
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
        if self.is_mouse_over(mx, my) and self.action:
            self.action()

def main():
    pygame.init()
    display = (1000, 750)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption('UI PG')

    init_gl(*display)
    running = True

    #Ruta en variable
    Start = "Textures\\Start.png"
    title = "Textures\\Title.png"

    # Cargar la imagen en la parte superior central
    Titulo = Button(-0.7, 0.1, 1.4, 0.8, (1.0, 1.0, 1.0), (0.8, 0.8, 0.8), title)


    buttons = [
       Button(-0.125, -0.9, 0.25, 0.15, (1.0, 1.0, 1.0), (0.8, 0.8, 0.8), Start, lambda: print("Hola")),
    ]

    clock = pygame.time.Clock()

    while running:
        mx, my = pygame.mouse.get_pos()
        # Convertir coordenadas del ratón de Pygame a coordenadas OpenGL
        mx = (mx / display[0]) * 2 - 1  # De 0..800 a -1..1
        my = 1 - (my / display[1]) * 2  # De 0..600 a 1..-1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    button.check_click(mx, my)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        for button in buttons:
            button.draw(mx, my)

        # Dibujar la imagen en la parte superior central
        Titulo.draw(mx, my)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
