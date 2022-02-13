from components.ambient.Diashow import Diashow
from utils.Animator import Animator
from utils.Transform import Transform


class Cannon(Diashow):

    OPENING_POS = (44., 1.)

    def __init__(self, duration: float = 0.1, transform: Transform = None):
        super().__init__([ "game.cannon0", "game.cannon1", "game.cannon2", "game.cannon3", "game.cannon4" ], duration, False, transform)
        self.animation.setRepeatMode(Animator.STOP)


    def getOpeningPos(self) -> tuple[float]:
        return self.transform.apply(Cannon.OPENING_POS)