from utils import Sprite
import pygame
import numpy as np

from utils.Animator import Animator

class CannonBall(Sprite):

    ANIM_TIME = 2.

    def __init__(self):
        super().__init__("game.cannon_ball", None, True, True, False)

        self.scaleAnim = Animator.easeOut(0.2, 0.5, CannonBall.ANIM_TIME / 2) + Animator.easeIn(0.5, 0.2, CannonBall.ANIM_TIME / 2)
        self.scaleAnim.setHook(lambda s : self.transform.setRelScale((s, s)))
        self.rotationAnim = Animator.lerp(0, 15, CannonBall.ANIM_TIME)
        self.rotationAnim.setHook(self.transform.setRelAngle)
        self.positionAnim = None
    
    def fire(self, start : tuple[float], dest : tuple[float]) -> None:
        start = np.array(start)
        dest = np.array(dest)

        def animFun(t : float):
            t /= CannonBall.ANIM_TIME
            basePos = dest * t + start * (1 - t)
            relExtraHeight = -4 * (t - 0.5)**2 + 1 # just parabola with zeros at 0, 1 and max at 0.5
            return basePos + np.array((0, -relExtraHeight * 70))

        self.positionAnim = Animator(animFun, CannonBall.ANIM_TIME)
        self.positionAnim.setHook(self.transform.setRelPosition)

        self.positionAnim.play()
        self.rotationAnim.play()
        self.scaleAnim.play()
    
    def draw(self, screen: pygame.Surface) -> None:
        if self.rotationAnim.isRunning():
            super().draw(screen)