import core.time
import glm



class Simulation:


    def __init__(self, resolution: int, type_: str) -> None:
        self.resolution = resolution
        self.type  = type_

        self.prey  = glm.vec3(15, 0, -50)
        self.point = glm.vec3(0)
        self.pred  = glm.vec3(0)

        self._lambda = 0

        # Speed
        self.alpha = 0.0054

        self.errors = []
        self.speed  = []

        self.iteration = -1

    def simulationOver(self):
        return glm.distance(self.prey, self.pred) < .3

    def updatePreyPosition(self):
        # Movement rectiligne
        if self.type == 'r':
            self.prey += glm.vec3(0, core.time.Time.FIXED_DELTA_TIME, 0)


    def run(self):
        self.iteration += 1

    def getReferenceVectors(self):
        pass

    def getError(self):
        pass