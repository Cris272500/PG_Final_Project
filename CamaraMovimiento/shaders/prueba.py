import pygame
import moderngl
import pywavefront
import numpy as np
import math

# Cargar el modelo OBJ con sus materiales
scene = pywavefront.Wavefront('projectPG.obj', collect_faces=True, create_materials=True)

# Cargar las texturas desde los materiales
textures = {}
for material in scene.materials.values():
    if hasattr(material, 'texture') and material.texture:
        image_path = material.texture.path
        image_surface = pygame.image.load(image_path)
        texture = pygame.image.tostring(image_surface, 'RGBA', True)
        width, height = image_surface.get_size()
        textures[material.name] = (texture, width, height)

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

def main():
    global z_pos

    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, pygame.OPENGL | pygame.DOUBLEBUF)
    ctx = moderngl.create_context()

    # Vertex Shader
    vertex_shader = """
    #version 330 core
    layout(location = 0) in vec3 in_position;
    layout(location = 1) in vec3 in_normal;
    layout(location = 2) in vec2 in_texcoord;
    
    out vec3 fragmentColor;
    out vec2 fragmentTexCoord;
    out vec3 fragmentNormal;
    
    uniform mat4 model;
    uniform mat4 view;
    uniform mat4 projection;
    
    void main() {
        gl_Position = projection * view * model * vec4(in_position, 1.0);
        fragmentTexCoord = in_texcoord;
        fragmentColor = vec3(1.0, 1.0, 1.0); // Color por defecto
        fragmentNormal = in_normal;
    }
    """

    # Fragment Shader
    fragment_shader = """
    #version 330 core
    in vec3 fragmentColor;
    in vec2 fragmentTexCoord;
    in vec3 fragmentNormal;
    
    out vec4 color;
    
    uniform sampler2D imageTexture;
    
    void main() {
        vec3 ambientColor = vec3(0.1, 0.1, 0.1);
        vec3 lightColor = vec3(1.0, 1.0, 1.0);
        vec3 lightDir = normalize(vec3(1.0, 1.0, 1.0)); // Dirección de la luz

        vec3 normal = normalize(fragmentNormal);
        float diff = max(dot(normal, lightDir), 0.0);

        vec3 diffuse = diff * lightColor;

        color = vec4((ambientColor + diffuse) * fragmentColor, 1.0) * texture(imageTexture, fragmentTexCoord);
    }
    """

    # Crear programa shader
    shader = ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)

    # Cargar datos del modelo
    vertices = []
    texcoords = []
    indices = []

    for mesh in scene.mesh_list:
        for face in mesh.faces:
            for vertex_i in face:
                vertex = scene.vertices[vertex_i]
                texcoord = getattr(scene, 'texcoords', None)[vertex_i] if hasattr(scene, 'texcoords') else [0, 0]
                vertices.extend(vertex)
                texcoords.extend(texcoord)

    vertices = np.array(vertices, dtype='f4')
    texcoords = np.array(texcoords, dtype='f4')

    # Crear VBO para vértices y texturas
    vbo_vertices = ctx.buffer(vertices.tobytes())
    vbo_texcoords = ctx.buffer(texcoords.tobytes())

    # Crear VAO
    vao = ctx.vertex_array(shader, [
        (vbo_vertices, '3f', 'in_position'),
        (vbo_texcoords, '2f', 'in_texcoord'),
    ])

    # Cargar la textura
    if textures:
        texture_name, (texture_data, width, height) = list(textures.items())[0]
        texture = ctx.texture((width, height), 4, texture_data)
        texture.use()

    # Crear la matriz de proyección
    fov = 45.0  # Ángulo de visión en grados
    near = 1.0
    far = 500.0
    aspect = display[0] / display[1]
    projection = np.array(perspective(fov, aspect, near, far), dtype='f4')

    # Crear la matriz de vista
    view = np.eye(4, dtype='f4')
    view[3, 2] = z_pos  # Establecer la posición z de la cámara

    # Crear la matriz de modelo
    model = np.eye(4, dtype='f4')
    model = model @ np.diag([*scene_scale, 1.0])
    model[3, :3] = scene_trans

    # Bucle principal
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    model = model @ np.array([
                        [1, 0, 0, -0.5],
                        [0, 1, 0, 0],
                        [0, 0, 1, 0],
                        [0, 0, 0, 1]
                    ], dtype='f4')
                if event.key == pygame.K_RIGHT:
                    model = model @ np.array([
                        [1, 0, 0, 0.5],
                        [0, 1, 0, 0],
                        [0, 0, 1, 0],
                        [0, 0, 0, 1]
                    ], dtype='f4')
                if event.key == pygame.K_UP:
                    z_pos += zoom_speed
                    view[3, 2] = z_pos
                if event.key == pygame.K_DOWN:
                    z_pos -= zoom_speed
                    view[3, 2] = z_pos
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
                    rot_x = np.array([
                        [1, 0, 0, 0],
                        [0, math.cos(math.radians(rotation[0])), -math.sin(math.radians(rotation[0])), 0],
                        [0, math.sin(math.radians(rotation[0])), math.cos(math.radians(rotation[0])), 0],
                        [0, 0, 0, 1]
                    ], dtype='f4')
                    rot_y = np.array([
                        [math.cos(math.radians(rotation[1])), 0, math.sin(math.radians(rotation[1])), 0],
                        [0, 1, 0, 0],
                        [-math.sin(math.radians(rotation[1])), 0, math.cos(math.radians(rotation[1])), 0],
                        [0, 0, 0, 1]
                    ], dtype='f4')
                    model = model @ rot_x @ rot_y

        ctx.clear(0.1, 0.1, 0.1)
        shader['projection'].write(projection)
        shader['view'].write(view)
        shader['model'].write(model)
        vao.render(moderngl.TRIANGLES)
        pygame.display.flip()

def perspective(fov, aspect, near, far):
    """Calcular la matriz de proyección perspectiva."""
    f = 1.0 / math.tan(fov * math.pi / 360.0)
    return [
        f / aspect, 0, 0, 0,
        0, f, 0, 0,
        0, 0, (far + near) / (near - far), -1,
        0, 0, (2 * far * near) / (near - far), 0
    ]

if __name__ == '__main__':
    main()


       
