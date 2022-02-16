import glfw
from typing import Any
from OpenGL.GL import *


from core.shader import Shader
from core.camera import Camera

import numpy as np
import glm


class Application:

    WIDTH  = 1000
    HEIGHT = 600

    m_Program: Shader
    m_Window: Any
    m_Camera: Camera

    def __init__(self, title="Window") -> None:
        if not glfw.init():
            raise Exception("glfw can not be initialized!")
        
        self.m_Window = glfw.create_window(self.WIDTH, self.HEIGHT, title, None, None)

        if not self.m_Window:
            glfw.terminate()
            raise Exception("glfw window can not be created!")

        glfw.set_window_pos(self.m_Window, 0, 0)

        # TODO Later
        glfw.make_context_current(self.m_Window)
        
        glViewport(0, 0, self.WIDTH, self.HEIGHT)
        glfw.set_window_size_callback(self.m_Window, self.onWindowSizeChange)

        glClearColor(0.0, 0.1, 0.0, 1.0)
        glEnable(GL_DEPTH_TEST)

        glfw.set_cursor_pos_callback(self.m_Window, self.mouseMove)

        self.m_Program = Shader('res/basic.vert', 'res/basic.frag')
        self.m_Program.use()

        self.createBuffer()

        # TODO REMOVE
        self.m_Camera = Camera(*([0]*6), 45.0, self.WIDTH / self.HEIGHT)

        self.deltaTime = 0
        self.lastFrame = 0

    def onWindowSizeChange(self, window, w, h):
        glViewport(0, 0, w, h)

    def processInput(self, key, x, y):
        pass

    def processMouse(self, button, state, x, y):
        pass

    def mouseMove(self, window, x, y):
        model = glm.mat4(1.0)
        model = glm.rotate(model, glm.radians(x), glm.vec3(0.0, 1.0, 0.0))
        self.m_Program.setMat4("model", np.matrix(model).T)


    def createBuffer(self):
        vertices = [-0.5, -0.5, 0.5, 1.0, 0.0, 0.0,
                    0.5, -0.5, 0.5, 0.0, 1.0, 0.0,
                    0.5,  0.5, 0.5, 0.0, 0.0, 1.0,
                    -0.5,  0.5, 0.5, 1.0, 1.0, 1.0,

                    -0.5, -0.5, -0.5, 1.0, 0.0, 0.0,
                    0.5, -0.5, -0.5, 0.0, 1.0, 0.0,
                    0.5,  0.5, -0.5, 0.0, 0.0, 1.0,
                    -0.5,  0.5, -0.5, 1.0, 1.0, 1.0]

        indices = [ 0, 1, 2, 2, 3, 0,
                    4, 5, 6, 6, 7, 4,
                    4, 5, 1, 1, 0, 4,
                    6, 7, 3, 3, 2, 6,
                    5, 6, 2, 2, 1, 5,
                    7, 4, 0, 0, 3, 7]

        vertices = np.array(vertices, dtype=np.float32)
        indices = np.array(indices, dtype=np.uint32)

        VBO = glGenBuffers(1)
        EBO = glGenBuffers(1)
        VAO = glGenVertexArrays(1)

        glBindVertexArray(VAO)

        glBindBuffer(GL_ARRAY_BUFFER, VBO)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 6 * 4, None)
        glEnableVertexAttribArray(0)

        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 6 * 4, ctypes.c_void_p(3 * 4))
        glEnableVertexAttribArray(1)


    def run(self) -> None:

        while not glfw.window_should_close(self.m_Window):
            currentFrame = glfw.get_time()
            self.deltaTime = currentFrame - self.lastFrame
            self.lastFrame = currentFrame

            glfw.set_window_title(self.m_Window, str(1.0 / self.deltaTime))

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            self.m_Program.use()

            self.m_Program.setMat4("projection", self.m_Camera.getProjectionMat())
            self.m_Program.setMat4("view", self.m_Camera.getViewMat())

            glDrawElements(GL_TRIANGLES, 6*6, GL_UNSIGNED_INT, None)
            
            glfw.poll_events()
            glfw.swap_buffers(self.m_Window)

        glfw.terminate()



        