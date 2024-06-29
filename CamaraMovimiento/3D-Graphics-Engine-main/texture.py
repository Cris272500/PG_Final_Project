import numpy as np
import moderngl as mgl
from PIL import Image

class Texture:
    def __init__(self, app):
        self.app = app
        self.ctx = app.ctx
        self.textures = {}
        self.load_textures()

    def load_textures(self):
        # Cargar texturas para el skybox
        self.textures['skybox'] = self.get_texture_cube(dir_path='textures/skybox1/', ext='png')

    def get_texture_cube(self, dir_path, ext='png'):
        faces = ['right', 'left', 'top', 'bottom', 'front', 'back']
        textures = []
        for face in faces:
            texture = Image.open(dir_path + f'{face}.{ext}').transpose(Image.FLIP_TOP_BOTTOM)
            texture_data = np.array(texture)
            textures.append(texture_data)

        size = textures[0].shape[:2][::-1]
        texture_cube = self.ctx.texture_cube(size=size, components=3, data=None)

        for i in range(6):
            texture_cube.write(data=textures[i], face=i)

        return texture_cube

    def destroy(self):
        [tex.release() for tex in self.textures.values()]
