import numpy as np
import sys

from core.components.transform import Transform
from core.entity import Entity

sys.path.append('..')

from core.components.cMesh import CMesh
from core.scene import Scene

class ObjParser:

    @staticmethod
    def parseMat(file_path: str):
        matStore: dict = {}
        matName : str = ""

        with open(file_path) as f:
            for line in f.readlines():
                if line.startswith("newmtl"):
                    matName = line.split()[1]
                elif line.startswith("Kd "):
                    r, g, b = [*map(float,line[3:].split()),]
                    matStore[matName] = [r, g, b, 1.0]

        return matStore

    @staticmethod
    def parse(scene: Scene, file_path: str, size=[1, 1, 1]) -> Entity:
        verts = []
        triangles = []
        colors = []
        matName: str = ""
        matStore: dict = None
        with open(file_path) as f:
            for line in f.readlines():
                if line.startswith('v '):
                    verts += [*map(float,line[2:].split()),]
                    

                elif line.startswith('f '):
                    i1, i2, i3 = [*map(lambda x:int(x)-1,line[2:].split()),]
                    
                    triangles += [verts[i1*3]*size[0], verts[i1*3+1]*size[1], verts[i1*3+2]*size[2]]
                    triangles += [verts[i2*3]*size[0], verts[i2*3+1]*size[1], verts[i2*3+2]*size[2]]
                    triangles += [verts[i3*3]*size[0], verts[i3*3+1]*size[1], verts[i3*3+2]*size[2]]

                    colors    += matStore[matName]*3 if matStore and matName in matStore else [0.0]*9

                elif line.startswith("mtllib"):
                    matFileName = line.split()[1]

                    matPath = "assets/"+matFileName
                    
                    matStore = ObjParser.parseMat(matPath)

                elif(line.startswith("usemtl") and matStore != None):
                    matName = line.split()[1]
                

        entt = scene.makeEntity()
        mesh: CMesh = entt.addComponent(CMesh)
        entt.addComponent(Transform, *([0]*6))

        mesh.m_Vertices  = np.array(triangles, dtype=np.float32)
        mesh.m_Colors    = np.array(colors, dtype=np.float32)

        mesh.buildMesh()

        return entt
