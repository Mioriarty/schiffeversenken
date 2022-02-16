
from re import S
from matplotlib.transforms import Transform
import pygame
from components.ui.AbstractButton import AbstractButton
from components.ui.ImageButton import ImageButton
from utils.Images import Sprite


class Checkbox(ImageButton):

    def __init__(self, scaleFactor : float = 0.8, inputLayer : int = AbstractButton.GAME_LAYER, transform : Transform = None):
        self.__substituteSprite = Sprite("buttons.checkbox_active")
        self.__isActive = False
        super().__init__("buttons.checkbox_idle", scaleFactor, inputLayer, transform)

        self.__substituteSprite.transform.setParent(self.transform)
        self.__substituteSprite.bakeTransform()
    
    def isActive(self) -> bool:
        return self.__isActive

    def toggle(self) -> None:
        self.__isActive = not self.__isActive
        self._sprite, self.__substituteSprite = self.__substituteSprite, self._sprite
    
    def onMouseUp(self) -> None:
        super().onMouseUp()
        self.toggle()
    
    def onPressCancel(self) -> None:
        super().onMouseUp()