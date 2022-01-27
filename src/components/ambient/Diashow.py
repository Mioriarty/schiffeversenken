from components.Component import Component
from utils import Transform
from scenes.Scene import SceneManager
import pygame
from utils.Animator import Animator
from utils.Images import Sprite


class Diashow(Component):

    def __init__(self, images : list[str | pygame.Surface], duration : float, drawLayer : int, transform : Transform = None):
        super().__init__(transform)
        self.sprites = [ Sprite(image, Transform.fromTransform(self.transform), bakeNow=True) for image in images ]

        self.animation = Animator.step(list(range(len(self.sprites))), duration * len(self.sprites))
        self.animation.setRepeatMode(Animator.RESTART)
        self.animation.play()

        SceneManager.putInDrawLayer(self, drawLayer)
    
    def draw(self, screen: pygame.Surface) -> None:
        self.sprites[self.animation.get()].draw(screen)

        