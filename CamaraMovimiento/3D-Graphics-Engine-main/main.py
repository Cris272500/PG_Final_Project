import pyrender
import numpy as np
import glfw
import trimesh  # Asegúrate de importar trimesh si es necesario
import moderngl as mgl  # Importa moderngl y asígnale el alias mgl

from scene import Scene  # Importa la clase Scene desde tu módulo scene.py
from vbo import VBO, SkyBoxVBO, AdvancedSkyBoxVBO  # Importa las clases VBO y sus derivadas

def main():
    # Configuración inicial del contexto
    glfw.init()
    window = glfw.create_window(800, 600, "OpenGL Viewer", None, None)
    glfw.make_context_current(window)
    
    # Crear contexto moderngl
    ctx = mgl.create_context()

    # Crear instancia de VBO y otras dependencias
    vbo = VBO(ctx)
    
    # Crear una instancia de Scene y pasar el contexto y otros recursos necesarios
    scene = Scene(ctx, vbo)
    
    # Iniciar el bucle principal
    while not glfw.window_should_close(window):
        # Procesar eventos
        glfw.poll_events()
        
        # Actualizar escena
        scene.update()
        
        # Renderizar escena
        scene.render()
        
        # Intercambiar buffers
        glfw.swap_buffers(window)
    
    # Limpiar al finalizar
    glfw.terminate()

if __name__ == "__main__":
    main()
