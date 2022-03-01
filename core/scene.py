import core.registry
import core.entity

class Scene:

    m_Registry: core.registry.Registry

    def __init__(self) -> None:
        self.m_Registry = core.registry.Registry()


    def makeEntity(self):
        __e = core.entity.Entity(self)
        self.m_Registry.registerEntity(__e)

        return __e


    