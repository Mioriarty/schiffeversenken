import numpy as np
from components.ambient.Diashow import Diashow
from utils.Transform import Transform
import random


class Bird(Diashow):
    """
    Represents a bird flying over the screen.
    """

    def __init__(self, duration: float = 0.2, velocity : float = 45., transform: Transform = None):
        """
        The construxtor of the Bird class.

        Args:
            duration (float, optional): Duration of one animation frame. Defaults to 0.2.
            velocity (float, optional): Movement speed of the bird. Defaults to 45.
            transform (Transform, optional): The Transform of the component. Defaults to None.
        """
        super().__init__(["ambient.bird1", "ambient.bird2", "ambient.bird3", "ambient.bird2"], duration, True, transform)
        self.velocity = velocity
        self.velocityDirection = None

        self.restart()

    def restart(self) -> None:
        """
        Restarts the movement. 

        The bird will be put to another side of the screen.
        """
        angle = random.random() * 2 * np.pi
        self.velocityDirection =  np.array(( np.cos(angle), np.sin(angle))) * self.velocity
        

        alongBorder = random.random() / 2 + 1/4
        offsetToBorder = (random.random() + 1/2) * 15

        if np.pi/4 <= angle <= np.pi * 3/4:
            # bird will spawn at the top
            self.transform.setRelPosition((alongBorder * 1024, -offsetToBorder))
        elif np.pi * 3/4 < angle <= np.pi * 5/4:
            # bird will spawn to the left
            self.transform.setRelPosition((1024 + offsetToBorder, alongBorder * 768))
        elif np.pi * 5/4 < angle <= np.pi * 7/4:
            # bird will spawn at the bottom
            self.transform.setRelPosition((alongBorder * 1024, 768 + offsetToBorder))
        else:
            # bird will spawn to the right
            self.transform.setRelPosition((-offsetToBorder, alongBorder * 768))
            



    def update(self, dt: float) -> None:
        self.transform.translate(dt * self.velocityDirection)

        if self.transform.getRelPosition()[0] < -50 or self.transform.getRelPosition()[1] < -50:
            self.restart()
        elif self.transform.getRelPosition()[0] > 1074 or self.transform.getRelPosition()[1] > 818:
            self.restart()

