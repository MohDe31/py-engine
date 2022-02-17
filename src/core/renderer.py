import core.components.camera
import core.shader
import core.scene


class Renderer:

    @staticmethod
    def render(scene: core.scene.Scene, shader: core.shader.Shader):
        cameras = scene.m_Registry.getAllOfType(core.components.camera.Camera)
        
        shader.use()
        for entity in cameras:
            camera: core.components.camera.Camera = cameras[entity][0]

            shader.setMat4("projection", camera.getProjectionMat())
            shader.setMat4("view", camera.getViewMat())

