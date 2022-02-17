import core.components.transform
import core.components.component

import glm



class Camera(core.components.component.Component):

    def __init__(self, entity, _fov, ratio, near=0.01, far=1000.0) -> None:
        super().__init__(entity)
        self.m_Projection = glm.perspective(glm.radians(_fov), ratio, near, far)

    def getProjectionMat(self):
        return self.m_Projection


    def getViewMat(self):
        #return glm.translate(glm.mat4(1.0), glm.vec3(0.0, 0.0, -5.0))
        #return glm.lookAt(self.m_Transform.m_Position, self.m_Transform.m_Position + self.m_Transform.front, self.m_Transform.up)
        __tr = self.m_Entity.getComponent(core.components.transform.Transform)
        assert __tr != None, "Transform doesn't exist"
        
        return glm.lookAt(__tr.m_Position, __tr.m_Position + __tr.front, __tr.up)