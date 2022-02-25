
import glfw
import glm

import core.components.transform
import core.components.camera
import core.application
import core.time
from core.primitives import cube, line
from neovec3D import NeuroVector3D
from utils.objparser import ObjParser


class Game:

    m_Application: core.application.Application

    frameCount: int = 0

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
                tr.setPosition(*(tr.m_Position + tr.right * core.time.Time.FIXED_DELTA_TIME * 5))

            if glfw.get_key(window, glfw.KEY_A):
                tr.setPosition(*(tr.m_Position - tr.right * core.time.Time.FIXED_DELTA_TIME * 5))

            if glfw.get_key(window, glfw.KEY_S):
                tr.setPosition(*(tr.m_Position - tr.front * core.time.Time.FIXED_DELTA_TIME * 5))

            if glfw.get_key(window, glfw.KEY_W):
                tr.setPosition(*(tr.m_Position + tr.front * core.time.Time.FIXED_DELTA_TIME * 5))

            if glfw.get_key(window, glfw.KEY_LEFT_CONTROL):
                tr.setPosition(*(tr.m_Position + glm.vec3(0, -core.time.Time.FIXED_DELTA_TIME * 5, 0)))

            if glfw.get_key(window, glfw.KEY_SPACE):
                tr.setPosition(*(tr.m_Position + glm.vec3(0, core.time.Time.FIXED_DELTA_TIME * 5, 0)))
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
        self.m_Application = application
        self.m_Application.m_ActiveScene = core.scene.Scene()
        camera_entity = self.m_Application.m_ActiveScene.makeEntity()
        tr_ = camera_entity.addComponent(core.components.transform.Transform, *([0]*6))
        camera_entity.addComponent(core.components.camera.Camera, 45.0, self.m_Application.WIDTH / self.m_Application.HEIGHT)

        glfw.set_input_mode(self.m_Application.m_Window, glfw.CURSOR, glfw.CURSOR_DISABLED)

        self.m_Application.setOnMouseMove(self.onMouseMove)

        tr_.setPosition(0,   0, 5)
        tr_.setRotation(0, -90, 0)

        self.cameraTransform = tr_

        self.m_Application.setProcessInputFunc(self.processInput)

        proie_OBJ = ObjParser.parse(self.m_Application.m_ActiveScene, 'assets/drone.obj')
        # proie_OBJ = self.m_Application.m_ActiveScene.makeEntity()
        # proie_OBJ.addComponent(core.components.transform.Transform, *([0]*6))
        pret_OBJ  = ObjParser.parse(self.m_Application.m_ActiveScene, 'assets/drone.obj')

        self._p0      = glm.vec3(0.0)

        self._proie = proie_OBJ.getComponent(core.components.transform.Transform).m_Position
        self._pret  = pret_OBJ.getComponent(core.components.transform.Transform).m_Position
        self._lambda  = 0

        self._proie.x = 15

        self.RES      = 50

        self.n_p0     = NeuroVector3D.fromCartesianVector(self._p0.x,    self._p0.y,    self._p0.z,     self.RES)
        self.n_pret   = NeuroVector3D.fromCartesianVector(self._pret.x,  self._pret.y,  self._pret.z,   self.RES)
        self.n_proie  = NeuroVector3D.fromCartesianVector(self._proie.x, self._proie.y, self._proie.z,  self.RES)

        objects = self.m_Application.m_ActiveScene.m_Registry.getAllOfType(core.components.camera.Camera)
        camera  = [*objects.keys(),][0]
        
        self.camPosition = camera.getComponent(core.components.transform.Transform).m_Position
        
        self._t = 0

    def update(self):
        if self._t: return

        if glm.distance(self._proie, self._pret) < .2:
            self._t = 1


        self.frameCount += 1

        self.n_pret   = NeuroVector3D.fromCartesianVector(self._pret.x,  self._pret.y,  self._pret.z,   self.RES)
        self.n_proie  = NeuroVector3D.fromCartesianVector(self._proie.x, self._proie.y, self._proie.z,  self.RES)

        rf  = (self.n_pret  - self.n_p0  ) * (self._lambda - 1)

        rpp = (self.n_proie - self.n_pret) *  self._lambda

        dt  = rpp + rf

        if self.frameCount == 1:
            self.c_lastpos = [self._proie.x, self._proie.y, self._proie.z]
            self.p_lastpos = [self._pret.x, self._pret.y, self._pret.z]

        self._pret   += glm.vec3(*NeuroVector3D.extractCartesianParameters(dt))

        self._lambda += 0.0054 * (1 - self._lambda)


        self._proie  += glm.vec3(0.0, core.time.Time.DELTA_TIME, core.time.Time.DELTA_TIME)

        # self.camPosition.x = self._proie.x
        # self.camPosition.y = self._proie.y
        # self.camPosition.z = self._proie.z

        if self.frameCount % 100 == 0 or self._t:
            line(self.m_Application.m_ActiveScene, self.c_lastpos, [self._proie.x, self._proie.y, self._proie.z])
            line(self.m_Application.m_ActiveScene, self.p_lastpos, [self._pret.x, self._pret.y, self._pret.z], [1, 0, 0])
            self.c_lastpos = [self._proie.x, self._proie.y, self._proie.z]
            self.p_lastpos = [self._pret.x, self._pret.y, self._pret.z]