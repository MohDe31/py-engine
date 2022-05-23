

class Entity:
    
    def __init__(self, scene) -> None:
        self.m_Scene    = scene
        self.m_isActive = True


    def addComponent(self, component, *args):
        return self.m_Scene.m_Registry.registerComponent(self, component, *args)

    def linkComponent(self, component):
        return self.m_Scene.m_Registry.linkComponent(self, component)

    def getComponent(self, component):
        return self.m_Scene.m_Registry.getComponent(self, component)