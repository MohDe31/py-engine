
import glfw, glm

import core.components.transform
import core.application
import core.time
from core.primitives import cube

class Game:

    lastX: float = 0
    lastY: float = 0
    mouseInit: bool = False

    cameraTransform: core.components.transform.Transform


    def __init__(self) -> None:
        (core.application.Application(init=self.initGame)).run(update=self.update)


    def processInput(self, window, activeScene):
        objs = activeScene.m_Registry.getAllOfTypes(core.components.camera.Camera, core.components.transform.Transform)
        
        # move this code to core
        for entity in objs:
            tr: core.components.transform.Transform = objs[entity][core.components.transform.Transform]
            if glfw.get_key(window, glfw.KEY_D):
                tr.setPosition(*(tr.m_Position + glm.vec3(core.time.Time.FIXED_DELTA_TIME, 0, 0)))

            if glfw.get_key(window, glfw.KEY_A):
                tr.setPosition(*(tr.m_Position + glm.vec3(-core.time.Time.FIXED_DELTA_TIME, 0, 0)))

            if glfw.get_key(window, glfw.KEY_S):
                tr.setPosition(*(tr.m_Position + glm.vec3(0, 0, core.time.Time.FIXED_DELTA_TIME)))

            if glfw.get_key(window, glfw.KEY_W):
                tr.setPosition(*(tr.m_Position + glm.vec3(0, 0, -core.time.Time.FIXED_DELTA_TIME)))

            if glfw.get_key(window, glfw.KEY_LEFT_CONTROL):
                tr.setPosition(*(tr.m_Position + glm.vec3(0, -core.time.Time.FIXED_DELTA_TIME, 0)))

            if glfw.get_key(window, glfw.KEY_SPACE):
                tr.setPosition(*(tr.m_Position + glm.vec3(0, core.time.Time.FIXED_DELTA_TIME, 0)))
            break

    def onMouseMove(self, w, xpos, ypos):
        if not self.mouseInit:
            self.lastX = xpos
            self.lastY = ypos
            self.mouseInit = True
        
        
        xOffset = xpos - self.lastX
        yOffset = self.lastY - ypos

        self.lastX = xpos
        self.lastY = ypos

        sensitivity = 2.0 * core.time.Time.FIXED_DELTA_TIME

        xOffset *= sensitivity
        yOffset *= sensitivity

        self.cameraTransform.rotate(yOffset, xOffset, 0)

        if self.cameraTransform.m_Rotation.x > 89.0:
            self.cameraTransform.setPitch(89.0)
        if self.cameraTransform.m_Rotation.x < -89.0:
            self.cameraTransform.setPitch(-89.0)

    def initGame(self, application: core.application.Application):
        # TODO Pack this stuff
        application.m_ActiveScene = core.scene.Scene()
        camera_entity = application.m_ActiveScene.makeEntity()
        tr_ = camera_entity.addComponent(core.components.transform.Transform, *([0]*6))
        camera_entity.addComponent(core.components.camera.Camera, 45.0, application.WIDTH / application.HEIGHT)

        glfw.set_input_mode(application.m_Window, glfw.CURSOR, glfw.CURSOR_DISABLED)

        application.setOnMouseMove(self.onMouseMove)

        tr_.setPosition(0,   0, 5)
        tr_.setRotation(0, -90, 0)

        self.cameraTransform = tr_

        application.setProcessInputFunc(self.processInput)

        cube(application.m_ActiveScene, [0, 0, 0])

    def update(self):
        pass
