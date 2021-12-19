from components.Component import Component
from utils import Transform
import pygame
import numpy as np


class AbstractButton(Component):

    def __init__(self, width : float, height : float, transform: Transform = Transform()):
        super().__init__(transform)
        self.width = width
        self.height = height

        self.__hovering = False
        self.__pressed = False
        self.__hoverCursor = pygame.SYSTEM_CURSOR_HAND

    def update(self, dt : float) -> None:
        relativeMousePos = np.absolute(self.transform.applyInv(pygame.mouse.get_pos()))
        hovering = 2 * relativeMousePos[0] <= self.width and 2 * relativeMousePos[1] <= self.height
        
        if hovering and not self.__hovering:
            pygame.mouse.set_cursor(self.__hoverCursor)
            self.onMouseEnter()
        elif not hovering and self.__hovering:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            if self.__pressed:
                self.onPressCancel()
                self.__pressed = False
            self.onMouseExit()

        self.__hovering = hovering
        
        if hovering:
            pressed = pygame.mouse.get_pressed()[0]

            if pressed and not self.__pressed:
                self.onMouseDown()
            elif not pressed and self.__pressed:
                self.onMouseUp()
                self.onClick()
            
            self.__pressed = pressed
                
        


    def onMouseEnter(self) -> None:
        pass

    def onMouseExit(self) -> None:
        pass

    def onMouseDown(self) -> None:
        pass

    def onMouseUp(self) -> None:
        pass

    def onPressCancel(self) -> None:
        pass

    def onClick(self) -> None:
        pass