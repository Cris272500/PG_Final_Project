import pyrender

class Scene:
    def __init__(self, ctx):
        self.ctx = ctx
        self.objects = []
        self.load()
        self.skybox = self.create_skybox()

    def add_object(self, obj):
        self.objects.append(obj)

    def load(self):
        gltf_file = 'projectPG.gltf'
        try:
            print(f"Cargando archivo: {gltf_file}")
            loaded = pyrender.Mesh.from_trimesh(pyrender.Mesh.from_trimesh)
            if loaded is None:
                raise ValueError(f"Error al cargar the archivo {gltf_file}: correctly")
 
