


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

    mesh_.m_Vertices = np.array([0.0, 0.0, 0.0, *(end-start)], dtype=np.float32)

    mesh_.m_Colors = np.array([*color, *color], dtype=np.float32)

    mesh_.buildMesh()

    return line_


def cube(scene: core.scene.Scene, position, global_scale=1):
    cube_ = scene.makeEntity()
    mesh_: core.components.mesh.Mesh = cube_.addComponent(core.components.mesh.Mesh)
    tr_ = cube_.addComponent(core.components.transform.Transform, *position, *([0]*3))
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
                                 -0.5,  0.5, -0.5], dtype=np.float32)*global_scale

    mesh_.m_Colors = np.array([1.0, 0.0, 0.0,
                               0.0, 1.0, 0.0,
                               0.0, 0.0, 1.0,
                               1.0, 1.0, 1.0,
                               1.0, 0.0, 0.0,
                               0.0, 1.0, 0.0,
                               0.0, 0.0, 1.0,
                               1.0, 1.0, 1.0], dtype=np.float32)

    mesh_.buildMesh()

    return cube_