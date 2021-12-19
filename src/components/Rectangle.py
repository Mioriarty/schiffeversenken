from components.Component import Component
from components.ui.AbstractButton import AbstractButton
from utils import Transform
import pygame

class Rectangle(AbstractButton):

    def __init__(self, transform: Transform, width : float, height : float):
        super().__init__(width, height, transform)
        self.width = width
        self.height = height
        self.color = (0, 0, 255)

    def draw(self, screen : pygame.Surface) -> None:
        polygon = self.transform.applyMultiple([(-self.width / 2, -self.height / 2), 
                                                (-self.width / 2,  self.height / 2),
                                                ( self.width / 2,  self.height / 2),
                                                ( self.width / 2, -self.height / 2)])

        pygame.draw.polygon(screen, self.color, polygon)
    
    def onMouseDown(self) -> None:
        self.color = (255, 0, 0)
    
    def onMouseUp(self) -> None:
        self.color = (0, 255, 0)

    def onPressCancel(self) -> None:
        self.color = (0, 100, 100)