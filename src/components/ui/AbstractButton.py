from typing import Callable
from components.Component import Component
from utils import Sounds, Transform
import pygame
import numpy as np


class AbstractButton(Component):

    def __init__(self, width : float, height : float, transform: Transform = None):
        super().__init__(transform)
        self.width = width
        self.height = height

        self.__hovering = False
        self.__pressed = False
        self.__hoverCursor = pygame.SYSTEM_CURSOR_HAND

        self.__onClickEvent : Callable[[], None] = None

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
                # actually call the onclick event
                if self.__onClickEvent is not None:
                    Sounds.playSoundEffect("click")
                    self.__onClickEvent()
            
            self.__pressed = pressed
                
    
    def setOnClickEvent(self, clickEvent : Callable[[], None]):
        self.__onClickEvent = clickEvent


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