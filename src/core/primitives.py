


import numpy as np

from OpenGL.GL import *

import core.components.transform
import core.components.mesh
import core.scene



def line(scene: core.scene.Scene, start, end, color = [0, 0, 0]):
    line_ = scene.makeEntity()
    mesh_: core.components.mesh.Mesh = line_.addComponent(core.components.mesh.Mesh, GL_LINES)
    tr_ = line_.addComponent(core.components.transform.Transform, *start, *([0]*3))
    mesh_.m_Triangles = np.array([ 0, 1 ], dtype=np.uint32)

    mesh_.m_Vertices = np.array([0.0, 0.0, 0.0, end[0] - start[0], end[1] - start[1], end[2] - start[2]], dtype=np.float32)

    mesh_.m_Colors = np.array([*color, *color], dtype=np.float32)

    mesh_.buildMesh()

    return line_


def cube(scene: core.scene.Scene, position):
    cube = scene.makeEntity()
    mesh_: core.components.mesh.Mesh = cube.addComponent(core.components.mesh.Mesh)
    tr_ = cube.addComponent(core.components.transform.Transform, *position, *([0]*3))
    mesh_.m_Triangles = np.array([ 0, 1, 2, 2, 3, 0,
                                   4, 5, 6, 6, 7, 4,
                                   4, 5, 1, 1, 0, 4,
                                   6, 7, 3, 3, 2, 6,
                                   5, 6, 2, 2, 1, 5,
                                   7, 4, 0, 0, 3, 7], dtype=np.uint32)

    mesh_.m_Vertices = np.array([-0.5, -0.5, 0.5,
                                 0.5, -0.5, 0.5, 
                                 0.5,  0.5, 0.5, 
                                 -0.5,  0.5, 0.5, 
                                 -0.5, -0.5, -0.5, 
                                 0.5, -0.5, -0.5, 
                                 0.5,  0.5, -0.5, 
                                 -0.5,  0.5, -0.5], dtype=np.float32)

    mesh_.m_Colors = np.array([1.0, 0.0, 0.0,
                               0.0, 1.0, 0.0,
                               0.0, 0.0, 1.0,
                               1.0, 1.0, 1.0,
                               1.0, 0.0, 0.0,
                               0.0, 1.0, 0.0,
                               0.0, 0.0, 1.0,
                               1.0, 1.0, 1.0], dtype=np.float32)

    mesh_.buildMesh()

    return tr_