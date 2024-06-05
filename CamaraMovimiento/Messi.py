import pygame
import OpenGL
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import pywavefront  # type: ignore

# Cargar el modelo OBJ
scene = pywavefront.Wavefront('PRUEBA2.obj', collect_faces=True)

# Calcular el tamaño del modelo y establecer la escala y la traslación
scene_box = (scene.vertices[0], scene.vertices[0])
for vertex in scene.vertices:
    min_v = [min(scene_box[0][i], vertex[i]) for i in range(3)]
    max_v = [max(scene_box[1][i], vertex[i]) for i in range(3)]
    scene_box = (min_v, max_v)

scene_size = [scene_box[1][i] - scene_box[0][i] for i in range(3)]
max_scene_size = max(scene_size)
scaled_size = 5
scene_scale = [scaled_size / max_scene_size for i in range(3)]
scene_trans = [-(scene_box[1][i] + scene_box[0][i]) / 2 for i in range(3)]

# Función para dibujar el modelo
def Model():
    glPushMatrix()
    glScalef(*scene_scale)
    glTranslatef(*scene_trans)

    for mesh in scene.mesh_list:
        glBegin(GL_TRIANGLES)
        for face in mesh.faces:
            for vertex_i in face:
                glVertex3f(*scene.vertices[vertex_i])
        glEnd()

    glPopMatrix()

# Función principal
def main():
    global mouse_down, last_pos, rotation, z_pos
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(45, (display[0] / display[1]), 1, 500.0)
    glTranslatef(0.0, 0.0, -10)

    mouse_down = False
    last_pos = None
    rotation = [0, 0]
    z_pos = -10
    zoom_speed = 2.0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    glTranslatef(-0.5, 0, 0)
                if event.key == pygame.K_RIGHT:
                    glTranslatef(0.5, 0, 0)
                if event.key == pygame.K_UP:
                     z_pos += zoom_speed # Acercar
                if event.key == pygame.K_DOWN:
                     z_pos -= zoom_speed  # Alejar
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Botón izquierdo del mouse
                    mouse_down = True
                    last_pos = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Botón izquierdo del mouse
                    mouse_down = False
            if event.type == pygame.MOUSEMOTION:
                if mouse_down:
                    current_pos = pygame.mouse.get_pos()
                    dx = current_pos[0] - last_pos[0]
                    dy = current_pos[1] - last_pos[1]
                    rotation[0] += dy
                    rotation[1] += dx
                    last_pos = current_pos

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glPushMatrix()
        glTranslatef(0.0, 0.0, z_pos)
        glRotatef(rotation[0], 1, 0, 0)
        glRotatef(rotation[1], 0, 1, 0)

        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        Model()
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

        glPopMatrix()

        pygame.display.flip()
        pygame.time.wait(10)

main()
