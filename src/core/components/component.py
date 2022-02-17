import core.entity


class Component:
    
    m_Enabled: bool
    m_Entity: core.entity.Entity

    def __init__(self, entity) -> None:
        self.m_Enabled = True
        self.m_Entity  = entity