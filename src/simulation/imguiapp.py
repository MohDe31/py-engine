from typing import List

import core.time
import numpy as np
import imgui



class ImGuiApp:


    selectedMovementMode: int = 0

    speed : List[float] = []
    errors: List[float] = []
    RESOLUTION: int     = 4

    def __init__(self) -> None:
        pass

    def startSimulationFunc(self):
        pass

    def render(self):
        imgui.begin("Control Panel", True)

        """
        imgui.text("Camera lock rotation")
        imgui.new_line()

        imgui.same_line()
        if imgui.button("Proie"):
            self.lookAtTarget = self._proie
        imgui.same_line()
        if imgui.button("Predateur"):
            self.lookAtTarget = self._pret
        imgui.same_line()
        if imgui.button("None"):
            self.lookAtTarget = None
        """
        
        _, self.selectedMovementMode = imgui.combo("Movement Mode", self.selectedMovementMode, ['Rectiligne', 'Hélicoïdale', 'Aléatoire'])
        _, self.RESOLUTION           = imgui.input_int("Resolution N", self.RESOLUTION)

        if self.RESOLUTION > 50:  self.RESOLUTION = 50
        elif self.RESOLUTION < 1: self.RESOLUTION = 1

        if len(self.errors):
            imgui.plot_lines("a°", np.array(self.errors, dtype=np.float32), overlay_text=f'avg: {sum(self.errors)/len(self.errors)}', graph_size=(0, 80))
            imgui.plot_lines("Speed", np.array(self.speed, dtype=np.float32), graph_size=(0, 80))
        else:
            imgui.plot_lines("a°", np.array([0], dtype=np.float32), overlay_text="avg: 0", graph_size=(0, 80))
            imgui.plot_lines("Speed", np.array([0], dtype=np.float32), graph_size=(0, 80))

        # _, core.time.Time.GAME_SPEED = imgui.drag_float("Simulation Speed", core.time.Time.GAME_SPEED, 0.01, 0.0, 1.0)


        if imgui.button("Start new simulation"):
            self.startSimulationFunc()

        imgui.end()