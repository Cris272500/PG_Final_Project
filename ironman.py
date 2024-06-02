from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from pywavefront import Wavefront

# Función para cargar el modelo OBJ
def cargar_modelo(filename):
    return Wavefront(filename)

# Función para renderizar el modelo OBJ
def renderizar_modelo(modelo):
    glBegin(GL_TRIANGLES)
    for name, material in modelo.materials.items():
        glColor(material.diffuse)
        for face in modelo.mesh_list:
            vertices = face.vertices
            for vertex_index in vertices:
                glVertex(vertex_index)
    glEnd()

# Función de visualización
def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glTranslatef(0.0, 0.0, -5.0)  # Ajusta la posición del modelo
    renderizar_modelo(modelo)
    glutSwapBuffers()

# Función para manejar el cambio de tamaño de la ventana
def reshape(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, (width / height), 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

# Inicialización de OpenGL y GLUT
glutInit()
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
glutInitWindowSize(800, 600)
glutInitWindowPosition(100, 100)
window = glutCreateWindow(b'Modelo OBJ con PyOpenGL')
glutDisplayFunc(display)
glutReshapeFunc(reshape)
glEnable(GL_DEPTH_TEST)

# Cargar el modelo OBJ
modelo = cargar_modelo('IronMan/IronMan.obj')

# Bucle principal de GLUT
glutMainLoop()

