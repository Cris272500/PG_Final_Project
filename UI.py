import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

# Inicialización de OpenGL
def init_gl(width, height):
    glClearColor(0.0, 0.0, 0.0, 1.0)  # Fondo negro
    glClearDepth(1.0)                 # Configuración de profundidad
    glEnable(GL_DEPTH_TEST)           # Activar la prueba de profundidad
    glDepthFunc(GL_LEQUAL)            # Tipo de prueba de profundidad
    glShadeModel(GL_SMOOTH)           # Sombreado suave
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(-1, 1, -1, 1)          # Configuración para vista ortográfica 2D
    glMatrixMode(GL_MODELVIEW)

# Clase para el botón
class Button:
    def __init__(self, x, y, width, height, color, hover_color, action=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.hover_color = hover_color
        self.action = action

    def draw(self, mx, my):
        if self.is_mouse_over(mx, my):
            glColor3f(*self.hover_color)
        else:
            glColor3f(*self.color)
        glBegin(GL_QUADS)
        glVertex2f(self.x, self.y)
        glVertex2f(self.x + self.width, self.y)
        glVertex2f(self.x + self.width, self.y + self.height)
        glVertex2f(self.x, self.y + self.height)
        glEnd()

    def is_mouse_over(self, mx, my):
        return self.x <= mx <= self.x + self.width and self.y <= my <= self.y + self.height

    def check_click(self, mx, my):
        if self.is_mouse_over(mx, my) and self.action:
            self.action()

def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption('Pygame OpenGL Multiple Buttons')

    init_gl(*display)
    running = True

    buttons = [
        Button(-0.8, 0.5, 0.25, 0.15, (0.0, 1.0, 0.0), (0.0, 0.8, 0.0), lambda: print("Hola")),
        #Button(0.3, 0.5, 0.5, 0.3, (0.0, 0.0, 1.0), (0.0, 0.0, 0.8), lambda: print("Button 2 Clicked!")),
        #Button(-0.8, -0.3, 0.5, 0.3, (1.0, 0.0, 0.0), (0.8, 0.0, 0.0), lambda: print("Button 3 Clicked!")),
       # Button(0.3, -0.3, 0.5, 0.3, (1.0, 1.0, 0.0), (0.8, 0.8, 0.0), lambda: print("Button 4 Clicked!"))
    ]

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

        pygame.display.flip()
        pygame.time.wait(10)

    pygame.quit()

if __name__ == "__main__":
    main()
