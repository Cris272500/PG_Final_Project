import pygame as PG
from OpenGL.GL import *

class App:
    def __init__(self):
        PG.init()
        PG.display.set_mode((640, 480), PG.OPENGL | PG.DOUBLEBUF)
        self.clock = PG.time.Clock()
        glClearColor(0.1, 0.2, 0.2, 1)
        self.mainloop()
    
    def mainloop(self):
        running = True
        while running:
            for event in PG.event.get():
                if event.type == PG.QUIT:
                    running = False
            glClear(GL_COLOR_BUFFER_BIT)
            PG.display.flip()
            self.clock.tick(60)
        self.quit()

    def quit(self):
        PG.quit()
    
if __name__ == '__main__':
    myapp = App()
    