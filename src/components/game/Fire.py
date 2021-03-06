from components.ambient.Diashow import Diashow
from utils.Transform import Transform
import random 


class Fire(Diashow):
    """
    Represents a fire on a ship.
    """

    def __init__(self, duration : float = 0.2, transform: Transform = None):
        """
        Constructor of fire class.

        Args:
            duration (float, optional): Duration of one image. Defaults to 0.2.
            transform (Transform, optional): Transform of the component. Defaults to None.
        """
        fireType = random.sample(list(range(2)), 1)[0]
        images = []

        if fireType == 0:
            images = [ "game.effects.fire11", "game.effects.fire12", "game.effects.fire13", "game.effects.fire12" ]
        elif fireType == 1:
            images = [ "game.effects.fire21", "game.effects.fire22", "game.effects.fire23", "game.effects.fire24" ]
        
        super().__init__(images, duration, True, transform)