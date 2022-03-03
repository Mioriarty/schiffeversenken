from components.ui.AbstractButton import AbstractButton
from utils.Images import Sprite
from utils.Input import Input
from utils.Transform import Transform
import pygame

class ImageButton(AbstractButton):
    """
    Represents a clickable image.

    It gets rescaled while clicking.
    """

    def __init__(self, image : str | pygame.Surface, scaleFactor : float = 0.8, inputLayer : int = Input.GAME_LAYER, transform : Transform = None):
        """
        The construcor of the ImageButton class.

        Args:
            image (str | pygame.Surface): Pygame surface or image name (see Images) of the clickable image.
            scaleFactor (float, optional): How much the image gets scaled while clicking. Defaults to 0.8.
            inputLayer (int, optional): The input layer of the button. Defaults to Input.GAME_LAYER.
            transform (Transform, optional): The Transform of the component. Defaults to None.
        """
        
        sprite = Sprite(image)
        super().__init__(sprite.image.get_width(), sprite.image.get_height(), inputLayer, transform)
        self._sprite = sprite
        self._sprite.transform.setParent(self.transform)
        self._sprite.bakeTransform()
        self.__scaleFactor = scaleFactor
    
    def onMouseDown(self) -> None:
        self._sprite.transform.scale(self.__scaleFactor)
        self._sprite.bakeTransform()
    
    def onMouseUp(self) -> None:
        self._sprite.transform.scale(1 / self.__scaleFactor)
        self._sprite.bakeTransform()
    
    def onPressCancel(self) -> None:
        self.onMouseUp()
    
    def draw(self, screen: pygame.Surface) -> None:
        self._sprite.draw(screen)