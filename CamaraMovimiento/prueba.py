import pygame
import moderngl
import pywavefront
import numpy as np
import math

# Cargar el modelo OBJ
scene = pywavefront.Wavefront('bunny.obj', collect_faces=True, create_materials=True)

# Calcular el tamaño del modelo y establecer la escala y la traslación
scene_box = (scene.vertices[0], scene.vertices[0])
for vertex in scene.vertices:
    min_v = [min(scene_box[0][i], vertex[i]) for i in range(3)]
    max_v = [max(scene_box[1][i], vertex[i]) for i in range(3)]
    scene_box = (min_v, max_v)

scene_size = [scene_box[1][i] - scene_box[0][i] for i in range(3)]
max_scene_size = max(scene_size)
scaled_size = 5
scene_scale = [scaled_size / max_scene_size for _ in range(3)]
scene_trans = [-(scene_box[1][i] + scene_box[0][i]) / 2 for i in range(3)]

# Variables de control
mouse_down = False
last_pos = None
rotation = [0, 0]
z_pos = -10
zoom_speed = 2.0

# Función principal
def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, pygame.OPENGL | pygame.DOUBLEBUF)
    ctx = moderngl.create_context()

    # Vertex Shader
    vertex_shader = """
    #version 330
    in vec3 in_position;
    in vec3 in_color;
    out vec3 color;
    uniform mat4 model;
    uniform mat4 view;
    uniform mat4 projection;
    void main() {
        gl_Position = projection * view * model * vec4(in_position, 1.0);
        color = in_color;
    }
    """

    # Fragment Shader
    fragment_shader = """
    #version 330
    in vec3 color;
    out vec4 fragColor;
    void main() {
        fragColor = vec4(color, 1.0);
    }
    """

    # Crear programa shader
    shader = ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)

    # Crear VAO y VBO
    vbo = ctx.buffer(np.array(scene.vertices, dtype='f4'))
    vao = ctx.simple_vertex_array(shader, vbo, 'in_position', 'in_color')

    # Crear la matriz de proyección
    fov = 45.0  # Ángulo de visión en grados
    near = 1.0
    far = 500.0
    # Variables de control
    mouse_down = False
    last_pos = None
    rotation = [0, 0]
    z_pos = -10
    zoom_speed = 2.0
    aspect = display[0] / display[1]
    projection = np.array(perspective(fov, aspect, near, far), dtype='f4')

    # Crear la matriz de vista
    view = np.array(np.eye(4), dtype='f4')
    view = view.dot(np.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, -1, z_pos],
        [0, 0, 0, 1]
    ], dtype='f4'))

    # Crear la matriz de modelo
    model = np.array(np.eye(4), dtype='f4')
    model = model.dot(np.array([
        [scene_scale[0], 0, 0, scene_trans[0]],
        [0, scene_scale[1], 0, scene_trans[1]],
        [0, 0, scene_scale[2], scene_trans[2]],
        [0, 0, 0, 1]
    ], dtype='f4'))

    # Bucle principal
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    model = model.dot(np.array([
                        [1, 0, 0, -0.5],
                        [0, 1, 0, 0],
                        [0, 0, 1, 0],
                        [0, 0, 0, 1]
                    ], dtype='f4'))
                if event.key == pygame.K_RIGHT:
                    model = model.dot(np.array([
                        [1, 0, 0, 0.5],
                        [0, 1, 0, 0],
                        [0, 0, 1, 0],
                        [0, 0, 0, 1]
                    ], dtype='f4'))
                if event.key == pygame.K_UP:
                    z_pos += zoom_speed
                    view = view.dot(np.array([
                        [1, 0, 0, 0],
                        [0, 1, 0, 0],
                        [0, 0, 1, zoom_speed],
                        [0, 0, 0, 1]
                    ], dtype='f4'))
                if event.key == pygame.K_DOWN:
                    z_pos -= zoom_speed
                    view = view.dot(np.array([
                        [1, 0, 0, 0],
                        [0, 1, 0, 0],
                        [0, 0, 1, -zoom_speed],
                        [0, 0, 0, 1]
                    ], dtype='f4'))
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
                    model = model.dot(np.array([
                        [1, 0, 0, 0],
                        [0, math.cos(math.radians(rotation[0])), -math.sin(math.radians(rotation[0])), 0],
                        [0, math.sin(math.radians(rotation[0])), math.cos(math.radians(rotation[0])), 0],
                        [0, 0, 0, 1]
                    ], dtype='f4')).dot(np.array([
                        [math.cos(math.radians(rotation[1])), 0, math.sin(math.radians(rotation[1])), 0],
                        [0, 1, 0, 0],
                        [-math.sin(math.radians(rotation[1])), 0, math.cos(math.radians(rotation[1])), 0],
                        [0, 0, 0, 1]
                    ], dtype='f4'))

        ctx.clear()
        shader['model'].write(model)
        shader['view'].write(view)
        shader['projection'].write(projection)
        vao.render(moderngl.TRIANGLES)
        pygame.display.flip()

def perspective(fov, aspect, near, far):
    """Calcular la matriz de proyección perspectiva."""
    f = 1.0 / math.tan(fov * math.pi / 360.0)
    return [
        f / aspect, 0, 0, 0,
        0, f, 0, 0,
        0, 0, (near + far) / (near - far), -1,
        0, 0, 2 * near * far / (near - far), 0
    ]

main()