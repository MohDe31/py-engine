


import math
import numpy as np

from OpenGL.GL import *

import core.components.transform
import core.components.mesh
import core.scene



def line(scene: core.scene.Scene, start, end, color = [0, 0, 0, 1]):
    line_ = scene.makeEntity()
    mesh_: core.components.mesh.Mesh = line_.addComponent(core.components.mesh.Mesh, GL_LINES)
    tr_ = line_.addComponent(core.components.transform.Transform, *start, *([0]*3))
    mesh_.m_Triangles = np.array([ 0, 1 ], dtype=np.uint32)

    mesh_.m_Vertices = np.array([0.0, 0.0, 0.0, *(end-start)], dtype=np.float32)

    mesh_.m_Colors = np.array([*color, *color], dtype=np.float32)

    mesh_.buildMesh()

    return line_


def cone(scene: core.scene.Scene, position, detail = 4, color = [0, 0, 0, 1], global_scale=[1, 1, 1]):
    cone_ = scene.makeEntity()
    mesh_: core.components.mesh.Mesh = cone_.addComponent(core.components.mesh.Mesh)
    cone_.addComponent(core.components.transform.Transform, *position, *([0]*3))

    step = 2 * math.pi / detail

    tris = []
    vs = []

    p = (0, global_scale[1], 0)

    vs += p
    for i in range(detail):
        a0 = step * i

        vs += [0.5*math.sin(a0) * global_scale[0], 0, 0.5*math.cos(a0)*global_scale[2]]
        pr = i if i > 0 else detail
        tris += [0, pr, i+1]
    mesh_.m_Triangles = np.array(tris, dtype=np.uint32)
    mesh_.m_Vertices  = np.array(vs, dtype=np.float32)
    colors = []
    for i in range(detail+1):
        colors+=color
    mesh_.m_Colors    = np.array(colors, dtype=np.float32)
    mesh_.buildMesh()

    return cone_

def cube(scene: core.scene.Scene, position, color = [0, 0, 0, 1], global_scale=[1, 1, 1]):
    cube_ = scene.makeEntity()
    mesh_: core.components.mesh.Mesh = cube_.addComponent(core.components.mesh.Mesh)
    cube_.addComponent(core.components.transform.Transform, *position, *([0]*3))
    mesh_.m_Triangles = np.array([ 0, 1, 2, 2, 3, 0,
                                   4, 5, 6, 6, 7, 4,
                                   4, 5, 1, 1, 0, 4,
                                   6, 7, 3, 3, 2, 6,
                                   5, 6, 2, 2, 1, 5,
                                   7, 4, 0, 0, 3, 7], dtype=np.uint32)

    mesh_.m_Vertices = np.array([-0.5 * global_scale[0], -0.5 * global_scale[1], 0.5 *  global_scale[2],
                                 0.5  * global_scale[0], -0.5 * global_scale[1], 0.5 *  global_scale[2], 
                                 0.5  * global_scale[0],  0.5 * global_scale[1], 0.5 *  global_scale[2], 
                                 -0.5 * global_scale[0],  0.5 * global_scale[1], 0.5 *  global_scale[2], 
                                 -0.5 * global_scale[0], -0.5 * global_scale[1], -0.5 * global_scale[2], 
                                 0.5  * global_scale[0], -0.5 * global_scale[1], -0.5 * global_scale[2], 
                                 0.5  * global_scale[0],  0.5 * global_scale[1], -0.5 * global_scale[2], 
                                 -0.5 * global_scale[0],  0.5 * global_scale[1], -0.5 * global_scale[2]], dtype=np.float32)

    mesh_.m_Colors = np.array([*color,
                               *color,
                               *color,
                               *color,
                               *color,
                               *color,
                               *color,
                               *color], dtype=np.float32)

    mesh_.buildMesh()

    return cube_


def cube2(scene: core.scene.Scene, position, color = [0, 0, 0, 1], global_scale=[1, 1, 1]):
    cube_ = scene.makeEntity()
    color2 = [.4, .4, .4, 1]
    mesh_: core.components.mesh.Mesh = cube_.addComponent(core.components.mesh.Mesh)
    cube_.addComponent(core.components.transform.Transform, *position, *([0]*3))
    mesh_.m_Triangles = np.array([ 0, 1, 2, 2, 3, 0,
                                   4, 5, 6, 6, 7, 4,
                                   4, 5, 1, 1, 0, 4,
                                   6, 7, 3, 3, 2, 6,
                                   5, 6, 2, 2, 1, 5,
                                   7, 4, 0, 0, 3, 7], dtype=np.uint32)

    mesh_.m_Vertices = np.array([-0.5 * global_scale[0], -0.5 * global_scale[1], 0.5 *  global_scale[2],
                                 0.5  * global_scale[0], -0.5 * global_scale[1], 0.5 *  global_scale[2], 
                                 0.5  * global_scale[0],  0.5 * global_scale[1], 0.3 *  global_scale[2], 
                                 -0.5 * global_scale[0],  0.5 * global_scale[1], 0.3 *  global_scale[2], 
                                 -0.5 * global_scale[0], -0.5 * global_scale[1], -0.5 * global_scale[2], 
                                 0.5  * global_scale[0], -0.5 * global_scale[1], -0.5 * global_scale[2], 
                                 0.5  * global_scale[0],  0.5 * global_scale[1], -0.3 * global_scale[2], 
                                 -0.5 * global_scale[0],  0.5 * global_scale[1], -0.3 * global_scale[2]], dtype=np.float32)

    mesh_.m_Colors = np.array([*color2,
                               *color2,
                               *color,
                               *color,
                               *color2,
                               *color2,
                               *color,
                               *color], dtype=np.float32)

    mesh_.buildMesh()

    return cube_