
import moderngl
import pyglet
from pyglet.gl import *
import numpy as np
import pyglet.graphics
import pyglet.window
import pywavefront
import moderngl_window as mglw
from pathlib import Path


class RenderEngine:
    def __init__(self, window):
        self.window = window
        self.ctx = moderngl.create_context()

        # Load the model
        self.model = self.load_model('assets/models/projectPG.obj')

        # Create shader program
        self.program = self.ctx.program(
            vertex_shader="""
            #version 330

            in vec3 in_position;
            in vec3 in_normal;

            uniform mat4 model;
            uniform mat4 view;
            uniform mat4 projection;

            out vec3 frag_normal;

            void main() {
                frag_normal = in_normal;
                gl_Position = projection * view * model * vec4(in_position, 1.0);
            }
            """,
            fragment_shader="""
            #version 330

            in vec3 frag_normal;
            out vec4 frag_color;

            void main() {
                vec3 normal = normalize(frag_normal);
                frag_color = vec4(abs(normal), 1.0);
            }
            """
        )

        # Setup buffers
        self.setup_buffers()

    def load_model(self, filename):
        obj = pywavefront.Wavefront(filename, parse=True)
        vertices = np.array(obj.vertices, dtype='f4')
        normals = np.array(obj.normals, dtype='f4')
        indices = np.array(obj.indices, dtype='i4')
        return {
            'vertices': vertices,
            'normals': normals,
            'indices': indices,
        }

    def setup_buffers(self):
        # Create VBOs
        self.vbo = self.ctx.buffer(self.model['vertices'].tobytes())
        self.nbo = self.ctx.buffer(self.model['normals'].tobytes())
        self.ibo = self.ctx.buffer(self.model['indices'].tobytes())

        # Create VAO
        self.vao = self.ctx.vertex_array(self.program, [
            (self.vbo, '3f', 'in_position'),
            (self.nbo, '3f', 'in_normal')
        ], index_buffer=self.ibo)

    def render(self):
        self.ctx.clear(0.2, 0.2, 0.2)
        self.vao.render(moderngl.TRIANGLES)

    def destroy(self):
        self.vao.release()
        self.vbo.release()
        self.nbo.release()
        self.ibo.release()
        self.program.release()


if __name__ == "__main__":
    # Create a Pyglet window
    window = pyglet.window.Window(width=800, height=600, caption='Modelo 3D')

    # Create an instance of RenderEngine
    render_engine = RenderEngine(window)

    @window.event
    def on_draw():
        window.clear()
        render_engine.render()

    pyglet.app.run()
