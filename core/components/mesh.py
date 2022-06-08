
import core.components.component
import core.entity
from OpenGL.GL import *
import numpy as np

import glm

class Mesh(core.components.component.Component):

    m_VBO: int
    m_VAO: int
    m_EBO: int

    m_Triangles: np.ndarray
    m_Vertices : np.ndarray
    m_Colors   : np.ndarray

    m_BlendColor: glm.vec4

    m_Type     : GLuint

    def __init__(self, entity: core.entity.Entity, meshType: GLuint = GL_TRIANGLES) -> None:
        super().__init__(entity)

        self.m_VBO = None
        self.m_VAO = None
        self.m_EBO = None

        self.m_Type = meshType
        self.m_BlendColor = glm.vec4(0.0)

    def buildMesh(self):
        if self.m_VBO == None:
            self.m_VBO = glGenBuffers(1)

        if self.m_EBO == None:
            self.m_EBO = glGenBuffers(1)

        if self.m_VAO == None:
            self.m_VAO = glGenVertexArrays(1)


        vts = self.m_Vertices.reshape(self.m_Vertices.size // 3,3)
        colors = self.m_Colors.reshape(self.m_Colors.size  // 4,4)
        vertices = np.hstack((vts, colors))
        sx, sy = vertices.shape

        vertices = vertices.reshape(sx * sy)

        glBindVertexArray(self.m_VAO)
        
        glBindBuffer(GL_ARRAY_BUFFER, self.m_VBO)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.m_EBO)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, 4 * self.m_Triangles.nbytes, self.m_Triangles, GL_STATIC_DRAW)

        # VERTICES
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 7 * 4, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)

        # COLOR
        glVertexAttribPointer(1, 4, GL_FLOAT, GL_FALSE, 7 * 4, ctypes.c_void_p(4 * 3))
        glEnableVertexAttribArray(1)