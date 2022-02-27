from components.ambient.Diashow import Diashow
from utils.Animator import Animator
from utils.Transform import Transform


class Cannon(Diashow):
    """
    Represents a Cannon on the land tzaht shoots the CannonBall.
    """

    OPENING_POS = (44., 1.)

    def __init__(self, duration: float = 0.1, transform: Transform = None):
        """
        Construcor of the Cannon class.

        Args:
            duration (float, optional): How long does one image stay. Defaults to 0.1.
            transform (Transform, optional): Transform of the component. Defaults to None.
        """
        super().__init__([ "game.cannon0", "game.cannon1", "game.cannon2", "game.cannon3", "game.cannon4" ], duration, False, transform)
        self.animation.setRepeatMode(Animator.STOP)


    def getOpeningPos(self) -> tuple[float]:
        """
        Returns where exactly the opening of the cannon is on the screen

        Returns:
            tuple[float]: Where exactly the opening of the cannon is on the screen
        """
        return self.transform.apply(Cannon.OPENING_POS)