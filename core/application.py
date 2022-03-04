import imgui
import glfw

from typing import Any
from OpenGL.GL import *


import core.components.transform
import core.components.camera
import core.components.mesh

import core.renderer
import core.shader
import core.scene
import core.time

from imgui.integrations.glfw import GlfwRenderer

class Application:

    WIDTH  = 1000
    HEIGHT = 600

    lastFrame: float = 0

    onMouseMove  = lambda _, w, x, y:None
    onMouseClick = lambda _, w, b, s, x, y:None
    processInputFunc = lambda _, w, s: None

    m_ActiveScene: core.scene.Scene
    m_Program: core.shader.Shader
    m_Window: Any

    def __init__(self, title="Window", init = lambda:None) -> None:
        if not glfw.init():
            raise Exception("glfw can not be initialized!")

        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)
        
        self.m_Window = glfw.create_window(self.WIDTH, self.HEIGHT, title, None, None)

        if not self.m_Window:
            glfw.terminate()
            raise Exception("glfw window can not be created!")

        
        glfw.set_window_pos(self.m_Window, 0, 0)

        glfw.make_context_current(self.m_Window)
        
        self.initImGUI()
        
        glViewport(0, 0, self.WIDTH, self.HEIGHT)
        glfw.set_window_size_callback(self.m_Window, self.onWindowSizeChange)

        glClearColor(1, 1, 1, 1)
        glEnable(GL_DEPTH_TEST)


        glfw.set_cursor_pos_callback(self.m_Window, self.mouseMove)

        self.m_Program = core.shader.Shader.load_basic()
        self.m_Program.use()
        
        init(self)


    def initImGUI(self):
        imgui.create_context()
        self.impl = GlfwRenderer(self.m_Window)

    def onWindowSizeChange(self, window, w, h):
        glViewport(0, 0, w, h)

    def processInput(self, window):
        self.processInputFunc(window, self.m_ActiveScene)

    def setProcessInputFunc(self, __func):
        self.processInputFunc = __func

    def setOnMouseMove(self, __func):
        self.onMouseMove = __func

    def setOnMouseClick(self, __func):
        self.onMouseClick = __func

    def processMouse(self, window, button, state, x, y):
        self.onMouseClick(window, button, state, x, y)

    def mouseMove(self, window, x, y):
        self.onMouseMove(window, x, y)


    def run(self, update = lambda:None) -> None:

        while not glfw.window_should_close(self.m_Window):
            glfw.poll_events()
            self.impl.process_inputs()
            currentFrame = glfw.get_time()
            core.time.Time.DELTA_TIME = currentFrame - self.lastFrame
            self.lastFrame = currentFrame

            glfw.set_window_title(self.m_Window, str(1.0 / core.time.Time.DELTA_TIME))

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)



            imgui.new_frame()

            update()

            imgui.render()

            self.processInput(self.m_Window)

            core.renderer.Renderer.render(self.m_ActiveScene, self.m_Program)
            
        
            self.impl.render(imgui.get_draw_data())

            glfw.swap_buffers(self.m_Window)

        glfw.terminate()



        