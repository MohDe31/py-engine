

import core.components.component

from typing import Dict, List


class Registry:

    m_Components: List[List[core.components.component.Component]] = []
    m_Entities:   Dict[int, object]     = {}
    m_Indices:    Dict[object, int]     = {}
    
    def __init__(self) -> None:
        pass


    def registerEntity(self, entity: object):
        assert entity not in self.m_Indices, "Entity already registered"
        
        self.m_Indices[entity] = len(self.m_Components)
        self.m_Entities[len(self.m_Components)] = entity

        self.m_Components.append([])

    def registerComponent(self, entity: object, component: type[core.components.component.Component], *args):
        assert entity in self.m_Indices, "Unknown entity"

        index = self.m_Indices[entity]
        entityComponents = self.m_Components[index]

        assert component not in map(type,entityComponents), "Entity already have this component"

        __comp = component(entity, *args)
        entityComponents.append(__comp)

        return __comp

    def getComponent(self, entity: object, type_: type[core.components.component.Component]):
        assert entity in self.m_Indices, "Unknown entity"

        index = self.m_Indices[entity]
        
        for component in self.m_Components[index]:
            if type(component) == type_:
                return component

        return None



    def getAllOfType(self, component: type[core.components.component.Component]):
        res = {}
        for entity in self.m_Indices:
            index = self.m_Indices[entity]
            __comp = [*filter(lambda x:type(x) == component, self.m_Components[index]),]
            if len(__comp):
                res[entity] = __comp


        return res


"""

ENTT2: [Transform]
ENTT1: [Transform, Camera]

[[RigidBody, Transform], [Transform, Camera, Health, Economy]]

{
    ETT1: 0,
    ETT2: 1
}

{
    0: ETT1,
    1: ETT2
}


map(lambda x:*x, C)

"""