import core.components.component

import numpy as np

from OpenGL.GL import *

class CMesh(core.components.component.Component):

    m_VBO: int
    m_VAO: int

    m_Vertices : np.ndarray
    m_Colors   : np.ndarray

    def __init__(self, entity: core.entity.Entity) -> None:
        super().__init__(entity)

        self.m_VBO = None
        self.m_VAO = None

    def buildMesh(self):
        if self.m_VBO == None:
            self.m_VBO = glGenBuffers(1)

        if self.m_VAO == None:
            self.m_VAO = glGenVertexArrays(1)


        vts = self.m_Vertices.reshape(self.m_Vertices.size // 3,3)
        colors = self.m_Colors.reshape(self.m_Colors.size // 3,3)
        vertices = np.hstack((vts, colors))
        sx, sy = vertices.shape

        vertices = vertices.reshape(sx * sy)

        glBindVertexArray(self.m_VAO)
        
        glBindBuffer(GL_ARRAY_BUFFER, self.m_VBO)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

        # VERTICES
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 6 * 4, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)

        # COLOR
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 6 * 4, ctypes.c_void_p(3 * 4))
        glEnableVertexAttribArray(1)
