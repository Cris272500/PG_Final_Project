import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

from Options import Credits
from button import Button  # Importa la clase Button

#Variables booleanas Globales
Cred = False
Sett = False

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

def ON_OFF_CREDITS():
    global Cred
    Cred = not Cred

def ON_OFF_SETTINGS():
    global Sett
    Sett = not Sett

def OFF_ALL():
    global Sett, Cred
    Sett, Cred = False, False

def main():
    pygame.init()
    display = (1000, 750)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption('UI PG')

    init_gl(*display)
    running = True

    #Ruta en variable
    Start = "Textures\\Start.png"
    Creditos = "Textures\\Credits_button.png"
    title = "Textures\\Title.png"
    Nombres = "Textures\\Credits.png"
    back = "Textures\\Return.png"
    Settings = "Textures\\Settings.png"

    # Cargar la imagen en la parte superior central
    Titulo = Button(-0.7, 0.1, 1.4, 0.8, (1.0, 1.0, 1.0), (0.8, 0.8, 0.8), title)
    Nombres_Proyecto = Button(-0.7, 0.1, 1.4, 0.8, (1.0, 1.0, 1.0), (0.8, 0.8, 0.8), Nombres)

    # Inicializar botones
    start_button = Button(-0.125, -0.9, 0.25, 0.17, (1.0, 1.0, 1.0), (0.8, 0.8, 0.8), Start, lambda: print("Hola"))
    credits_button = Button(-0.450, -0.93, 0.30, 0.24, (1.0, 1.0, 1.0), (0.8, 0.8, 0.8), Creditos, ON_OFF_CREDITS)
    back_button = Button(-0.700, -0.93, 0.25, 0.15, (1.0, 1.0, 1.0), (0.8, 0.8, 0.8), back, OFF_ALL)
    settings_button = Button(0.200, -0.9, 0.25, 0.15, (1.0, 1.0, 1.0), (0.8, 0.8, 0.8), Settings, ON_OFF_SETTINGS)

    #Activar o desactivar botones
    back_button.disable()
    Nombres_Proyecto.disable()

    buttons = [
       start_button,
       credits_button,
       back_button,
       Titulo,
       Nombres_Proyecto,
       settings_button,
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

        if Cred:
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glLoadIdentity()

            back_button.enable()
            Nombres_Proyecto.enable()

            start_button.disable()
            credits_button.disable()
            settings_button.disable()
            Titulo.disable()
        
        elif Sett:
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glLoadIdentity()



        else:
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glLoadIdentity()

            back_button.disable()
            Nombres_Proyecto.disable()

            start_button.enable()
            credits_button.enable()
            settings_button.enable()
            Titulo.enable()

        for button in buttons:
            button.draw(mx, my)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
