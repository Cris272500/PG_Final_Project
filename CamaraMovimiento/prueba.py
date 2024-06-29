import pygame as pg
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import numpy as np

def create_shader(vertex_filepath: str, fragment_filepath: str) -> int:
    """
    Compile and link shader modules to make a shader program.

    Parameters:
        vertex_filepath: path to the text file storing the vertex source code
        fragment_filepath: path to the text file storing the fragment source code
    
    Returns:
        A handle to the created shader program
    """

    with open(vertex_filepath, 'r') as f:
        vertex_src = f.read()

    with open(fragment_filepath, 'r') as f:
        fragment_src = f.read()
    
    shader = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER),
                            compileShader(fragment_src, GL_FRAGMENT_SHADER))
    
    return shader

class Mesh:
    """
    A mesh that can represent an obj model.
    """

    def __init__(self, filename: str):
        """
        Initialize the mesh.
        """

        vertices, colors = self.load_mesh(filename)
        self.vertex_count = len(vertices)

        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)

        # Vertices
        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, vertices, GL_STATIC_DRAW)
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)

        # Colors
        self.cbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.cbo)
        glBufferData(GL_ARRAY_BUFFER, colors, GL_STATIC_DRAW)
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 0, None)

    def load_mesh(self, filename: str) -> tuple:
        """
        Load a mesh from an obj file.

        Parameters:
            filename: the filename.
        
        Returns:
            The loaded data, in a flattened format.
        """

        vertices = []
        colors = []

        with open(filename, "r") as file:
            for line in file:
                if line.startswith('v '):
                    vertex = list(map(float, line.strip().split()[1:]))
                    vertices.extend(vertex)
                elif line.startswith('vc '):
                    color = list(map(float, line.strip().split()[1:]))
                    colors.extend(color)

        return np.array(vertices, dtype=np.float32), np.array(colors, dtype=np.float32)

    def arm_for_drawing(self) -> None:
        """
        Arm the triangle for drawing.
        """
        glBindVertexArray(self.vao)
    
    def draw(self) -> None:
        """
        Draw the triangle.
        """
        glDrawArrays(GL_TRIANGLES, 0, self.vertex_count)

    def destroy(self) -> None:
        """
        Free any allocated memory.
        """
        glDeleteVertexArrays(1, (self.vao,))
        glDeleteBuffers(1, (self.vbo,))
        glDeleteBuffers(1, (self.cbo,))

class App:
    """
    For now, the app will be handling everything.
    Later on we'll break it into subcomponents.
    """

    def __init__(self):

        self._set_up_pygame()
        self._set_up_opengl()
        self._create_assets()
        self._set_onetime_uniforms()

    def _set_up_pygame(self) -> None:
        """
        Initialize and configure pygame.
        """

        pg.init()
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)
        pg.display.set_mode((800, 600), pg.OPENGL|pg.DOUBLEBUF)

    def _set_up_opengl(self) -> None:
        """
        Configure any desired OpenGL options
        """

        glClearColor(0.1, 0.2, 0.2, 1)
        glEnable(GL_DEPTH_TEST)

    def _create_assets(self) -> None:
        """
        Create all of the assets needed for drawing.
        """

        self.cube_mesh = Mesh("models/projectPG.obj")
        self.shader = create_shader("shaders/vertex.txt", "shaders/fragment.txt")
        
    def _set_onetime_uniforms(self) -> None:
        """
        Some shader data only needs to be set once.
        """

        glUseProgram(self.shader)

        projection_transform = np.array([
            [1.81066096, 0.0, 0.0, 0.0],
            [0.0, 2.41421356, 0.0, 0.0],
            [0.0, 0.0, -1.002002, -0.2002002],
            [0.0, 0.0, -1.0, 0.0]
        ], dtype=np.float32)

        glUniformMatrix4fv(
            glGetUniformLocation(self.shader, "projection"),
            1, GL_FALSE, projection_transform
        )

    def run(self) -> None:
        """ Run the app """

        running = True
        while running:
            # Check events
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
            
            # Refresh screen
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glUseProgram(self.shader)

            # Arm mesh for drawing
            self.cube_mesh.arm_for_drawing()

            # Draw mesh
            self.cube_mesh.draw()

            pg.display.flip()

    def quit(self) -> None:
        """ Cleanup the app, run exit code """

        self.cube_mesh.destroy()
        glDeleteProgram(self.shader)
        pg.quit()

if __name__ == "__main__":
    my_app = App()
    my_app.run()
    my_app.quit()
