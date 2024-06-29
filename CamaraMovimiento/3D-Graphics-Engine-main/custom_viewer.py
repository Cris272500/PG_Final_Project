import glfw
import numpy as np
import pyrender

class CustomViewer(pyrender.Viewer):
    def __init__(self, scene, **kwargs):
        super().__init__(scene, **kwargs)
        self.key_down = set()
        self.move_speed = 0.05
        self.rot_speed = 0.02

    def key_callback(self, window, key, scancode, action, mods):
        if action == glfw.PRESS:
            self.key_down.add(key)
        elif action == glfw.RELEASE:
            self.key_down.discard(key)
        super().key_callback(window, key, scancode, action, mods)

    def rotate_camera(self, dx, dy):
        self._camera_pose = np.dot(self._camera_pose, pyrender.camera.rotate_around_x(dx * self.rot_speed))
        self._camera_pose = np.dot(self._camera_pose, pyrender.camera.rotate_around_y(dy * self.rot_speed))

    def step(self, *args, **kwargs):
        if glfw.KEY_W in self.key_down:
            self._camera_pose[2, 3] -= self.move_speed
        if glfw.KEY_S in self.key_down:
            self._camera_pose[2, 3] += self.move_speed
        if glfw.KEY_A in self.key_down:
            self._camera_pose[0, 3] -= self.move_speed
        if glfw.KEY_D in self.key_down:
            self._camera_pose[0, 3] += self.move_speed

        super().step(*args, **kwargs)
