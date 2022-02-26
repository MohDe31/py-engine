
from math import acos, degrees
from typing import List
import glfw
import glm
import numpy as np

import core.components.transform
import core.components.camera
import core.application
import core.time
from core.primitives import line
from neovec3D import NeuroVector3D
from utils.objparser import ObjParser

import imgui

class Game:

    movementMode = { 0: 'r', 1: 'h', 2: 'a' }
    selectedMovementMode: int = 0
    lockCamera: bool = False

    RESOLUTION: int = 4

    m_Application: core.application.Application

    frameCount: int = 0

    lastX: float = 0
    lastY: float = 0

    mouseInit: bool = False
    cursor   : bool = True

    lines: List[object] = []
    errors: List[float] = []

    cameraTransform: core.components.transform.Transform


    def __init__(self) -> None:
        (core.application.Application(init=self.initGame)).run(update=self.update)


    def processInput(self, window, activeScene):
        
        if glfw.get_key(window, glfw.KEY_ESCAPE) and imgui.is_key_pressed(256):
            self.cursor = not self.cursor
            glfw.set_input_mode(self.m_Application.m_Window, glfw.CURSOR, glfw.CURSOR_NORMAL if self.cursor else glfw.CURSOR_DISABLED)
            self.mouseInit = False


        if self.cursor: return
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
        if self.cursor: return

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

        # glfw.set_input_mode(self.m_Application.m_Window, glfw.CURSOR, glfw.CURSOR_DISABLED)

        self.m_Application.setOnMouseMove(self.onMouseMove)

        tr_.setPosition(0,   0, 5)
        tr_.setRotation(0, -90, 0)

        self.cameraTransform = tr_

        self.m_Application.setProcessInputFunc(self.processInput)


        # proie_OBJ = self.m_Application.m_ActiveScene.makeEntity()
        # proie_OBJ.addComponent(core.components.transform.Transform, *([0]*6))
        self.proie_OBJ = ObjParser.parse(self.m_Application.m_ActiveScene, 'assets/drone.obj')
        self.pret_OBJ  = ObjParser.parse(self.m_Application.m_ActiveScene, 'assets/drone.obj')

        self._proie   = self.proie_OBJ.getComponent(core.components.transform.Transform).m_Position
        self._pret    = self.pret_OBJ.getComponent(core.components.transform.Transform).m_Position


        self.lookAtTarget = None
        self.initScene()

    def initScene(self):
        for line in self.lines:
            self.m_Application.m_ActiveScene.m_Registry.removeEntity(line)

        self.used_resolution       = self.RESOLUTION

        self.errors.clear()
        self.lines.clear()
        self.frameCount = 0

        self._p0      = glm.vec3(0.0)
        self._lambda  = 0

        self._proie.x = 15
        self._proie.y = 0
        self._proie.z = 0

        self._pret.x  = 0
        self._pret.y  = 0
        self._pret.z  = 0

        self._t = 0

    def initRandom(self):
        self.initScene()

    def update(self):


        imgui.begin("Control Panel", True)

        imgui.text("Camera lock rotation")
        imgui.new_line()

        imgui.same_line()
        if imgui.button("Proie"):
            self.lookAtTarget = self._proie
        imgui.same_line()
        if imgui.button("Predateur"):
            self.lookAtTarget = self._pret
        imgui.same_line()
        if imgui.button("None"):
            self.lookAtTarget = None

        
        _, self.selectedMovementMode = imgui.combo("Movement Mode", self.selectedMovementMode, ['Rectiligne', 'Hélicoïdale', 'Aléatoire'])
        _, self.RESOLUTION           = imgui.input_int("Resolution N", self.RESOLUTION)

        if self.RESOLUTION > 50:  self.RESOLUTION = 50
        elif self.RESOLUTION < 1: self.RESOLUTION = 1

        if len(self.errors):
            imgui.plot_lines("a°", np.array(self.errors, dtype=np.float32), overlay_text=f'avg: {sum(self.errors)/len(self.errors)}', graph_size=(0, 80))
        else:
            imgui.plot_lines("a°", np.array([0], dtype=np.float32), overlay_text="avg: 0", graph_size=(0, 80))

        _, core.time.Time.GAME_SPEED = imgui.drag_float("Simulation Speed", core.time.Time.GAME_SPEED, 0.01, 0.0, 1.0)



        if imgui.button("Start new simulation"):
            self.initRandom()

        imgui.end()

        # imgui.show_test_window()

        if core.time.Time.GAME_SPEED == 0: return
        if self._t: return

        if glm.distance(self._proie, self._pret) < .3:
            self._t = 1


        self.frameCount += 1

        rf  = self._pret - self._p0
        rpp = self._proie - self._pret

        rf  = NeuroVector3D.fromCartesianVector(*rf, self.used_resolution ) * (self._lambda - 1)
        rpp = NeuroVector3D.fromCartesianVector(*rpp, self.used_resolution) *  self._lambda
        
        dt  = rpp + rf

        if self.frameCount == 1:
            self.c_lastpos = [self._proie.x, self._proie.y, self._proie.z]
            self.p_lastpos = [self._pret.x, self._pret.y, self._pret.z]


        self._pret += glm.vec3(*NeuroVector3D.extractCartesianParameters(dt))

        rf   = self._pret  - self._p0
        rpp  = self._proie - self._pret

        self._lambda += core.time.Time.GAME_SPEED * 0.0054 * (1 - self._lambda)


        self._proie  += glm.vec3(0.0, core.time.Time.DELTA_TIME, core.time.Time.DELTA_TIME) * core.time.Time.GAME_SPEED

        if self.lookAtTarget != None:
            self.cameraTransform.lookAt(self.lookAtTarget)

        if self.frameCount % 100 == 0 or self._t:
            self.lines.append(line(self.m_Application.m_ActiveScene, self.c_lastpos, [self._proie.x, self._proie.y, self._proie.z]))
            self.lines.append(line(self.m_Application.m_ActiveScene, self.p_lastpos, [self._pret.x, self._pret.y, self._pret.z], [1, 0, 0]))

            self.c_lastpos = [self._proie.x, self._proie.y, self._proie.z]
            self.p_lastpos = [self._pret.x, self._pret.y, self._pret.z]

            v12  = glm.length(rf) * glm.length(rpp)
            
            cosa = glm.dot(rf, rpp) / v12

            self.errors.append(degrees(acos(cosa if cosa <= 1 else 1)))