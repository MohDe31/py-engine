import numpy as np
import core.time
import glm



class Simulation:


    def __init__(self, resolution: int, type_: str) -> None:
        self.resolution = resolution
        self.type  = type_
        
        if self.type == 'r' :
            self.prey  = glm.vec3(15, 0, -50)

        elif self.type == 'h' :
            self.z = np.linspace(-2*np.pi, 2*np.pi, 1000)
            self.prey = glm.vec3(np.cos(self.z[0]), np.sin(self.z[0]), self.z[0])

        elif self.type == 'a' :
            self.prey = glm.vec3(15, 0, 0)
            self.v = glm.vec3(0, .01, .01)

        self.point = glm.vec3(0)
        self.pred  = glm.vec3(0)

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
        # Movement helicoidale 
        if self.type == 'h':
            self.prey.x = np.cos(self.z[self.iteration+2])
            self.prey.y = np.sin(self.z[self.iteration+2])
            self.prey.z = self.z[self.iteration+2]
        # Movement Aleatoire
        if self.type == 'a' :
            self.prey += self.v
            if self.iteration % 10 == 0 :
                axis = [glm.vec3(1, 0, 0), glm.vec3(0, 1, 0), glm.vec3(0, 0, 1)]
                np.random.shuffle(axis)
                self.v = glm.rotate(self.v, np.pi/9, axis[0])



    def run(self):
        self.iteration += 1

    def getReferenceVectors(self):
        pass

    def getError(self):
        pass