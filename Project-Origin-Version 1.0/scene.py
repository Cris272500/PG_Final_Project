from model import *
import glm


class Scene:
    def __init__(self, app):
        self.app = app
        self.objects = []
        self.load()
        # skybox
        self.skybox = AdvancedSkyBox(app)

    def add_object(self, obj):
        self.objects.append(obj)

    def load(self):
        app = self.app
        add = self.add_object

   

        # cat
        add(Cat(app, pos=(0, -1, -10)))
        add(Cesped(app, pos=(0, 1.3, -5)))
        add(Detalles(app, pos=(0, -1, -10)))
        add(Vestuario(app, pos=(0, 1.3, -14)))
        add(Vest(app, pos=(0, 1.3, -10)))
        add(Trophy(app, pos=(-5, 1, -35)))
        add(Champions(app, pos=(0, 1.3, -12)))
        add(Mundial(app, pos=(0, 1.3, -17)))
        add(Ball(app, pos=(0, 1.3, -19)))
        add(SerieA(app, pos=(0, 1.3, -21)))




