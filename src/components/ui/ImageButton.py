from components.ui.AbstractButton import AbstractButton
from scenes.Scene import SceneManager
from utils.Images import Sprite
from utils.Transform import Transform
import pygame

class ImageButton(AbstractButton):

    def __init__(self, sprite : Sprite, scaleFactor : float = 0.8, inputLayer : int = AbstractButton.GAME_LAYER, transform : Transform = None):
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