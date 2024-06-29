import pygltflib

def load_model(filename):
    model = pygltflib.GLTF2().load(filename)

    vertices = []
    normals = []
    indices = []

    for mesh in model.meshes:
        for primitive in mesh.primitives:
            positions = model.accessors[primitive.attributes.POSITION].view.to_list()
            if primitive.attributes.NORMAL:
                normals = model.accessors[primitive.attributes.NORMAL].view.to_list()
            indices = model.accessors[primitive.indices].view.to_list()

            vertices.extend(positions)

    return {
        'vertices': vertices,
        'normals': normals,
        'indices': indices,
    }
