

class Entity:
    
    def __init__(self, scene) -> None:
        self.m_Scene = scene


    def addComponent(self, component, *args):
        return self.m_Scene.m_Registry.registerComponent(self, component, *args)

    def getComponent(self, component):
        return self.m_Scene.m_Registry.getComponent(self, component)