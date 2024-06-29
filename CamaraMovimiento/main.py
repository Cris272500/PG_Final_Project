import pyglet
import moderngl
from pyglet.gl import *
import numpy as np
from pathlib import Path
from mesh_loader import load_model
from shader import load_shader


class RenderEngine:
    def __init__(self, window):
        self.window = window
        self.ctx = moderngl.create_context()

        # Load the model using mesh_loader
        self.model = load_model('assets/models/projectPG.glb')

        # Create shader program using shader module
        self.program = load_shader(self.ctx)

        # Setup buffers
        self.setup_buffers()

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
