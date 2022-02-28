from simulation.simulation import Simulation
from simulation.fixedpoint import FixedPoint
from simulation.infinitpoint import InfinitPoint
from simulation.imguiapp import ImGuiApp

from typing import List

from utils.objparser import ObjParser

from core.primitives import cube, line
import core.components.transform
import core.components.camera
import core.application
import core.time

import imgui
import glfw
import glm

class Game:

    movementMode = { 0: 'r', 1: 'h', 2: 'a' }
    camouflageMode = {0: 'f', 1: 'i'}
    lockCamera: bool = False

    m_Application: core.application.Application

    lastX: float = 0
    lastY: float = 0

    mouseInit: bool = False
    cursor   : bool = True

    lines : List[object] = []

    cameraTransform: core.components.transform.Transform

    imGuiApp: ImGuiApp
    simulation: Simulation = None

    def __init__(self) -> None:
        (core.application.Application(init=self.initGame)).run(update=self.update)

    def initGame(self, application: core.application.Application):
        self.m_Application = application
        self.m_Application.m_ActiveScene = core.scene.Scene()

        # Creating an entity
        camera_entity = self.m_Application.m_ActiveScene.makeEntity()
        # Giving the entity a transform
        self.cameraTransform = camera_entity.addComponent(core.components.transform.Transform, 0, 0, 5, 0, -90, 0)
        # Adding a camera component
        camera_entity.addComponent(core.components.camera.Camera, 45.0, self.m_Application.WIDTH / self.m_Application.HEIGHT)

        # Setting the input events
        self.m_Application.setOnMouseMove(self.onMouseMove)
        self.m_Application.setProcessInputFunc(self.processInput)

        # Loading the drone objects
        self.preyTransform = ObjParser.parse(self.m_Application.m_ActiveScene, 'assets/drone.obj').getComponent(core.components.transform.Transform)
        self.predTransform = ObjParser.parse(self.m_Application.m_ActiveScene, 'assets/drone.obj').getComponent(core.components.transform.Transform)

        self.initApp()


    def initApp(self):
        self.imGuiApp = ImGuiApp()
        self.imGuiApp.startSimulationFunc = self.startSimulation


    def clearScene(self):
        for line in self.lines:
            self.m_Application.m_ActiveScene.m_Registry.removeEntity(line)
        
        self.lines.clear()

    def startSimulation(self):
        self.clearScene()

        mode = self.movementMode[self.imGuiApp.selectedMovementMode]
        
        if self.camouflageMode[self.imGuiApp.selectedCamouflageMode] == 'f' :
           self.simulation = FixedPoint(self.imGuiApp.RESOLUTION, mode)
        elif self.camouflageMode[self.imGuiApp.selectedCamouflageMode] == 'i' :
           self.simulation = InfinitPoint(self.imGuiApp.RESOLUTION, mode)
           
        self.onStartNew()

    def onStartNew(self):
        self.predTransform.m_Position = self.simulation.pred
        self.preyTransform.m_Position = self.simulation.prey


    def update(self):
        self.imGuiApp.render()
        if not self.simulation:return
        # imgui.show_test_window()
        self.simulation.run()

        self.imGuiApp.errors = self.simulation.errors
        self.imGuiApp.speed  = self.simulation.speed

        if self.camouflageMode[self.imGuiApp.selectedCamouflageMode] == 'f':
            if self.simulation.iteration == 1:
                self.c_lastpos = glm.vec3(*self.simulation.prey)
                self.p_lastpos = glm.vec3(*self.simulation.pred)

                self.lines.append(cube(self.m_Application.m_ActiveScene, self.simulation.pred, .1))


            # Line drawing stuff!!
            if self.simulation.iteration > 1 and self.simulation.iteration % 60 == 0:
                self.lines.append(line(self.m_Application.m_ActiveScene, self.c_lastpos, self.simulation.prey))
                self.lines.append(line(self.m_Application.m_ActiveScene, self.p_lastpos, self.simulation.pred, [1, 0, 0]))
                self.lines.append(cube(self.m_Application.m_ActiveScene, self.simulation.pred, .1))

                self.lines.append(line(self.m_Application.m_ActiveScene, self.simulation.point, self.simulation.prey, [1, 0, 1]))

                self.c_lastpos = glm.vec3(*self.simulation.prey)
                self.p_lastpos = glm.vec3(*self.simulation.pred)
        else:
            if self.simulation.iteration == 1:
                self.c_lastpos = glm.vec3(*self.simulation.prey)
                self.p_lastpos = glm.vec3(*self.simulation.pred)

            if self.simulation.iteration > 1 and self.simulation.iteration % 60 == 0:
                self.lines.append(line(self.m_Application.m_ActiveScene, self.c_lastpos, self.simulation.prey))
                self.lines.append(line(self.m_Application.m_ActiveScene, self.p_lastpos, self.simulation.pred))
                self.lines.append(line(self.m_Application.m_ActiveScene, self.simulation.prey, self.simulation.pred, [1, 0, 0]))


                self.c_lastpos = glm.vec3(*self.simulation.prey)
                self.p_lastpos = glm.vec3(*self.simulation.pred)


        """
        if core.time.Time.GAME_SPEED == 0: return



        if self.lookAtTarget != None:
            self.cameraTransform.lookAt(self.lookAtTarget)
        """




    
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