from typing import Callable
from components.ambient.Diashow import Diashow
from utils import Sprite
import pygame
import numpy as np

from utils.Animator import Animator
from utils.Sounds import Sounds
from utils.Transform import Transform

class CannonBall(Sprite):

    ANIM_TIME = .0001 # TODO 1.5

    def __init__(self, animFinishedCallback : Callable[[tuple[float], bool], None]):
        super().__init__("game.cannon_ball", None, True, True, False)

        self.scaleAnim = Animator.easeOut(0.2, 0.5, CannonBall.ANIM_TIME / 2) + Animator.easeIn(0.5, 0.2, CannonBall.ANIM_TIME / 2)
        self.scaleAnim.setHook(lambda s : self.transform.setRelScale((s, s)))
        self.scaleAnim.setRepeatMode(Animator.STOP)

        self.rotationAnim = Animator.lerp(0, 15, CannonBall.ANIM_TIME)
        self.rotationAnim.setHook(self.transform.setRelAngle)
        self.rotationAnim.setEndCallback(self.__flightFinished)
        self.rotationAnim.setRepeatMode(Animator.STOP)

        self.positionAnim = Animator(None, CannonBall.ANIM_TIME)
        self.positionAnim.setHook(self.transform.setRelPosition)
        self.positionAnim.setRepeatMode(Animator.STOP)

        self.isHittingShot = True
        self.animFinishedCallback = animFinishedCallback

        self.splash = Diashow(
            [ "game.effects.splash1", "game.effects.splash2", "game.effects.splash3", "game.effects.splash4", "game.effects.splash5", "game.effects.splash6", "game.effects.splash7" ], 
            0.2, False, 
            Transform(scale=(0.6, 0.6))
        )
        self.splash.animation.setRepeatMode(Animator.STOP)

        self.explosion = Diashow(
            [ "game.effects.explosion1", "game.effects.explosion2", "game.effects.explosion3", "game.effects.explosion4", "game.effects.explosion5", "game.effects.explosion6"],
            0.2, False,
            Transform(scale=(0.8, 0.8))
        )
        self.explosion.animation.setRepeatMode(Animator.STOP)

    
    def fire(self, start : tuple[float], dest : tuple[float], hits : bool) -> None:
        self.isHittingShot = hits
        Sounds.playSoundEffect("cannon")

        if hits:
            self.explosion.transform.setRelPosition(dest)
            self.explosion.animation.setEndCallback(lambda : self.animFinishedCallback(dest, hits))
        else:
            self.splash.transform.setRelPosition(dest)
            self.splash.animation.setEndCallback(lambda : self.animFinishedCallback(dest, hits))

        
        start = np.array(start)
        dest = np.array(dest)

        def animFun(t : float):
            t /= CannonBall.ANIM_TIME
            basePos = dest * t + start * (1 - t)
            relExtraHeight = -4 * (t - 0.5)**2 + 1 # just parabola with zeros at 0, 1 and max at 0.5
            return basePos + np.array((0, -relExtraHeight * 70))

        self.positionAnim.setEquation(animFun)
        
        self.positionAnim.play()
        self.rotationAnim.play()
        self.scaleAnim.play()
    
    def __flightFinished(self) -> None:
        if self.isHittingShot:
            Sounds.playSoundEffect("explosion")
            self.explosion.animation.play()
        else:
            Sounds.playSoundEffect("splash")
            self.splash.animation.play()
            
    
    def draw(self, screen: pygame.Surface) -> None:
        if self.rotationAnim.isRunning():
            super().draw(screen)
        elif self.splash.animation.isRunning():
            self.splash.draw(screen)
        elif self.explosion.animation.isRunning():
            self.explosion.draw(screen)