import pygame as pg
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import numpy as np

def create_shader(vertex_filepath: str, fragment_filepath: str) -> int:
    """
        Compilar y enlazar módulos de sombreado para crear un programa de sombreado.
        Parámetros:

            vertex_filepath: ruta al archivo de texto que contiene el
                             código fuente del vertex shader
            
            fragment_filepath: ruta al archivo de texto que contiene el
                               código fuente del fragment shader
        Devuelve:

            Un manejador al programa de sombreado creado
    """
    with open(vertex_filepath, 'r') as f:
        vertex_src = f.readlines()

    with open(fragment_filepath, 'r') as f:
        fragment_src = f.readlines()
    
    shader = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER),
                            compileShader(fragment_src, GL_FRAGMENT_SHADER))
    return shader

class App:
    """
        Por ahora, la aplicación manejará todo.
        Más adelante lo dividiremos en subcomponentes.
    """
    def __init__(self):
        """ Inicializar el programa """
        self._set_up_pygame()

        self._set_up_timer()

        self._set_up_opengl()

        self._create_assets()

        self._set_onetime_uniforms()
    
    def _set_up_pygame(self) -> None:
        """
            Inicializar y configurar pygame.
        """
        pg.init()
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK,
                                    pg.GL_CONTEXT_PROFILE_CORE)
        pg.display.set_mode((640, 480), pg.OPENGL | pg.DOUBLEBUF)

    def _set_up_timer(self) -> None:
        """
            Configurar el temporizador de la aplicación.
        """
        self.clock = pg.time.Clock()
    
    def _set_up_opengl(self) -> None:
        """
            Configurar las opciones deseadas de OpenGL.
        """
        glClearColor(0.1, 0.2, 0.2, 1)
        # ajustando blending
        # Elblending es la combinacion de colores
        glDisable(GL_BLEND)
        # glBlendFunc(GL_ONE, GL_ZERO)
    
    def _create_assets(self) -> None:
        """
            Crear todos los recursos necesarios para el dibujo.
        """

        self.Cuadrado = Cuadrado()
        self.wood_texture = Material("gfx/adoquin.jpg")
        self.shader = create_shader(
            vertex_filepath="shaders/vertex.txt", 
            fragment_filepath="shaders/fragment.txt")
    
    def _set_onetime_uniforms(self) -> None:
        """
            Algunos datos del shader solo necesitan ser configurados una vez.
        """
        glUseProgram(self.shader)
        glUniform1i(glGetUniformLocation(self.shader, "imageTexture"), 0)

    def run(self) -> None:
        """ Ejecutar la aplicación """

        running = True
        while running:
            # Verificar eventos
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
            # Refrescar pantalla
            glClear(GL_COLOR_BUFFER_BIT)

            glUseProgram(self.shader)
            self.wood_texture.use()
            self.Cuadrado.arm_for_drawing()
            self.Cuadrado.draw()

            pg.display.flip()

            # Temporización
            self.clock.tick(60)

    def quit(self) -> None:
        """ Limpiar la aplicación, ejecutar código de salida """

        self.Cuadrado.destroy()
        self.wood_texture.destroy()
        glDeleteProgram(self.shader)
        pg.quit()

class Cuadrado:
    def __init__(self):
        """
            Inicializar 
        """

        # x, y, z, r, g, b, s, t
        vertices = (
            # posiciones      # colores        # coordenadas de textura
            -0.5, -0.5, 0.0,  1.0, 0.0, 0.0,  0.0, 0.0,  # abajo-izquierda
             0.5, -0.5, 0.0,  0.0, 1.0, 0.0,  1.0, 0.0,  # abajo-derecha
             0.5,  0.5, 0.0,  0.0, 0.0, 1.0,  1.0, 1.0,  # arriba-derecha
            -0.5,  0.5, 0.0,  1.0, 1.0, 0.0,  0.0, 1.0   # arriba-izquierda
        )
        indices = (
            0, 1, 2,  # primer triángulo
            2, 3, 0   # segundo triángulo
        )
        vertices = np.array(vertices, dtype=np.float32)
        indices = np.array(indices, dtype=np.uint32)
        self.vertex_count = len(indices)

        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)
        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
        self.ebo = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.ebo)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(0))
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(12))
        glEnableVertexAttribArray(2)
        glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(24))

    def arm_for_drawing(self) -> None:
        glBindVertexArray(self.vao)
    
    def draw(self) -> None:
        glDrawElements(GL_TRIANGLES, self.vertex_count, GL_UNSIGNED_INT, None)

    def destroy(self) -> None:
        glDeleteVertexArrays(1, (self.vao,))
        glDeleteBuffers(1, (self.vbo,))
        glDeleteBuffers(1, (self.ebo,))

class Material:
    """
        Una textura básica.
    """
    def __init__(self, filepath: str):
        """
            Inicializar y cargar la textura.
            Parámetros:
                filepath: ruta al archivo de imagen.
        """
        self.texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        image = pg.image.load(filepath).convert_alpha()
        image_width, image_height = image.get_rect().size
        img_data = pg.image.tostring(image, 'RGBA')
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image_width, image_height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
        glGenerateMipmap(GL_TEXTURE_2D)

    def use(self) -> None:
        """
            Preparar la textura para el dibujo.
        """
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.texture)

    def destroy(self) -> None:
        """
            Liberar la textura.
        """
        glDeleteTextures(1, (self.texture,))

my_app = App()
my_app.run()
my_app.quit()
