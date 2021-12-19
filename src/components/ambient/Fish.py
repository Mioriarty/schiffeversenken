from components.Component import Component
from utils import Transform, Animator
import pygame

class Fish(Component):

    def __init__(self, initalPosition : list | tuple):
        super().__init__(Transform(initalPosition))

        self.horizontalAnimation = Animator.oscillate(initalPosition[0], initalPosition[0] - 100, 10)
        self.horizontalAnimation.setRepeatMode(Animator.RESTART)
        self.horizontalAnimation.setHook(self.transform.setRelXPos)
        self.horizontalAnimation.play()

        self.verticalAnimation = Animator.oscillate(initalPosition[1]-20, initalPosition[1]+20, 3)
        self.verticalAnimation.setRepeatMode(Animator.RESTART)
        self.verticalAnimation.setHook(self.transform.setRelYPos)
        self.verticalAnimation.play()

        self.flipAnimation = Animator.const(1.0, 4) + Animator.smoothLerp(1.0, -1.0, 1) + Animator.const(-1.0, 4) + Animator.smoothLerp(-1.0, 1.0, 1.0)
        self.flipAnimation.setRepeatMode(Animator.RESTART)
        self.flipAnimation.setHook(self.transform.setRelXScale)
        self.flipAnimation.play()

    
    def draw(self, screen : pygame.Surface) -> None:
        pos = self.transform.getPosition()
        scale = self.transform.getScale() * 30.0
        pygame.draw.ellipse(screen, (255, 255, 0), [pos[0], pos[1], scale[0], scale[1]])