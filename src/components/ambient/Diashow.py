from components.Component import Component
from utils import Transform
import pygame
from utils.Animator import Animator
from utils.Images import Sprite


class Diashow(Component):

    def __init__(self, images : list[str | pygame.Surface], duration : float, repeat : bool = True, transform : Transform = None):
        super().__init__(transform)
        self.sprites = [ Sprite(image, Transform(parent=self.transform), bakeNow=True) for image in images ]

        self.animation = Animator.step(list(range(len(self.sprites))), duration * len(self.sprites))
        
        if repeat:
            self.animation.setRepeatMode(Animator.RESTART)
            self.animation.play()
    
    def draw(self, screen: pygame.Surface) -> None:
        self.sprites[self.animation.get()].draw(screen)

        