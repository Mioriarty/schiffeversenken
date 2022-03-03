from components.Component import Component
from utils import Transform
import pygame
from utils.Animator import Animator
from utils.Images import Sprite


class Diashow(Component):
    """
    Represents a simple stop-motion-like animation.

    Here, different images a played in quick succession.
    """

    def __init__(self, images : list[str | pygame.Surface], duration : float, repeat : bool = True, transform : Transform = None):
        """
        Constructor of the Diashow class.

        Args:
            images (list[str | pygame.Surface]): The images that should be shown after another.
            duration (float): The duration of one image.
            repeat (bool, optional): Whether the animation should repeat endlessly. Defaults to True.
            transform (Transform, optional): The trabsform of the component. Defaults to None.
        """
        super().__init__(transform)
        self.sprites = [ Sprite(image, Transform(parent=self.transform), bakeNow=True) for image in images ]

        self.animation = Animator.step(list(range(len(self.sprites))), duration * len(self.sprites))
        
        if repeat:
            self.animation.setRepeatMode(Animator.RESTART)
            self.animation.play()
    
    def draw(self, screen: pygame.Surface) -> None:
        self.sprites[self.animation.get()].draw(screen)

        