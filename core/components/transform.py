from math import atan2, cos, degrees, sin, acos, asin, sqrt

import numpy as np

import core.components.component
import core.entity

import glm


class Transform(core.components.component.Component):

    WORLD_UP = glm.vec3(0.0, 1.0, 0.0)

    def __init__(self, entity: core.entity.Entity, x: float, y: float, z: float, pitch: float, yaw: float, roll: float) -> None:
        super().__init__(entity)

        self.m_Position = glm.vec3(x, y, z)
        self.m_Rotation = glm.vec3(pitch, yaw, roll)

        self.updateVectors()


    def setPosition(self, x: float, y: float, z: float):
        self.m_Position.x = x
        self.m_Position.y = y
        self.m_Position.z = z

    def setRotation(self, pitch: float, yaw: float, roll: float):
        self.m_Rotation.x = pitch
        self.m_Rotation.y = yaw
        self.m_Rotation.z = roll

        self.updateVectors()

    def setPitch(self, value):
        self.m_Rotation.x = value
        self.updateVectors()


    def setYaw(self, value):
        self.m_Rotation.y = value
        self.updateVectors()


    def setRoll(self, value):
        self.m_Rotation.z = value
        self.updateVectors()


    def rotate(self, pitch: float, yaw: float, roll: float):
        self.m_Rotation.x += pitch
        self.m_Rotation.y += yaw
        self.m_Rotation.z += roll

        self.updateVectors()
    
    def lookAt(self, target: glm.vec3):
        target = glm.normalize(target - self.m_Position)
        self.front = target

        # self.m_Rotation.x = degrees(atan2(target.z, target.x))
        # print(atan2(target.y, target.x))
        # self.m_Rotation.y = degrees((np.pi / 2 if target.x > 0 else -np.pi/2) - acos(target.z))
        # print(self.m_Rotation.y)
        # self.updateVectors()

    def updateVectors(self):
        self.front = glm.vec3(
            cos(glm.radians(self.m_Rotation.y)) * cos(glm.radians(self.m_Rotation.x)),
            sin(glm.radians(self.m_Rotation.x)),
            sin(glm.radians(self.m_Rotation.y)) * cos(glm.radians(self.m_Rotation.x))
        )

        self.front = glm.normalize(self.front)

        self.right = glm.normalize(glm.cross(self.front, Transform.WORLD_UP))
        self.up    = glm.normalize(glm.cross(self.right, self.front))