import numpy as np
import glm

from core.transform import Transform


class Camera:

    def __init__(self, xPos, yPos, zPos, pitch, yaw, roll, _fov, ratio, near=0.01, far=1000.0) -> None:
        self.m_Transform  = Transform(xPos, yPos, zPos, pitch, yaw, roll)
        self.m_Projection = np.matrix(glm.perspective(glm.radians(_fov), ratio, near, far)).T

    def getProjectionMat(self):
        return self.m_Projection


    def getViewMat(self):
        return np.matrix(glm.translate(glm.mat4(1.0), glm.vec3(0.0, 0.0, -5.0))).T
        #return glm.lookAt(self.m_Transform.m_Position, self.m_Transform.m_Position + self.m_Transform.front, self.m_Transform.up)