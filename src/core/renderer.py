import core.components.transform
import core.components.camera
import core.components.mesh
import core.shader
import core.scene

from OpenGL.GL import *

import glm

class Renderer:

    @staticmethod
    def render(scene: core.scene.Scene, shader: core.shader.Shader):
        cameras = scene.m_Registry.getAllOfType(core.components.camera.Camera)
        
        shader.use()
        for entity in cameras:
            camera: core.components.camera.Camera = cameras[entity][0]

            shader.setMat4("projection", camera.getProjectionMat())
            shader.setMat4("view", camera.getViewMat())

            break

        mesh_objects = scene.m_Registry.getAllOfTypes(core.components.mesh.Mesh, core.components.transform.Transform)

        for entity in mesh_objects:
            components: dict = mesh_objects[entity]
            
            mesh     : core.components.mesh.Mesh           = components[core.components.mesh.Mesh]
            transform: core.components.transform.Transform = components[core.components.transform.Transform]

            glBindVertexArray(mesh.m_VAO)

            model = glm.mat4(1.0)
            model = glm.translate(model, glm.vec3(*transform.m_Position))
            model = glm.rotate(model, transform.m_Rotation.x, glm.vec3(1.0, 0.0, 0.0))
            model = glm.rotate(model, transform.m_Rotation.y, glm.vec3(0.0, 1.0, 0.0))
            model = glm.rotate(model, transform.m_Rotation.z, glm.vec3(0.0, 0.0, 1.0))

            shader.setMat4("model", model)
            

            glDrawElements(GL_TRIANGLES, 6*6, GL_UNSIGNED_INT, None)
