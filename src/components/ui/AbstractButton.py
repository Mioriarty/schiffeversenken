from typing import Callable
from components.Component import Component
from utils import Sounds, Transform
import pygame
import numpy as np

from utils.Input import Input


class AbstractButton(Component):

    GAME_LAYER = 0
    UI_LAYER = 1

    __crntInputLayer = GAME_LAYER

    def __init__(self, width : float, height : float, inputLayer : int, transform: Transform = None):
        super().__init__(transform)
        self.width = width
        self.height = height
        self.inputLayer = inputLayer

        self.__enabled = True
        self.__hovering = False
        self.__pressed = False
        self.__hoverCursor = pygame.SYSTEM_CURSOR_HAND

        self.__onClickEvent : Callable[[], None] = None

    def update(self, dt : float) -> None:
        if self.__enabled and AbstractButton.__crntInputLayer == self.inputLayer:
            relativeMousePos = np.absolute(self.transform.applyInv(Input.getMousePos()))
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
                clicked = Input.hasEvent(pygame.MOUSEBUTTONDOWN) and Input.getEvent(pygame.MOUSEBUTTONDOWN).button == 1

                if clicked:
                    self.onMouseDown()
                    self.__pressed = True
                elif self.__pressed:
                    released = Input.hasEvent(pygame.MOUSEBUTTONUP) and Input.getEvent(pygame.MOUSEBUTTONUP).button == 1
                    if released:
                        self.onMouseUp()
                        
                        # actually call the onclick event
                        if self.__onClickEvent is not None:
                            Sounds.playSoundEffect("click")
                            self.__onClickEvent()
                        self.__pressed = False
                    
    
    def setOnClickEvent(self, clickEvent : Callable[[], None]):
        self.__onClickEvent = clickEvent

    def addOnClickEvent(self, clickEvent : Callable[[], None]) -> None:
        if self.__onClickEvent is None:
            self.__onClickEvent = clickEvent
        else:
            oldEvent = self.__onClickEvent
            def newEvent():
                oldEvent()
                clickEvent()
            self.__onClickEvent = newEvent
    
    def enable(self) -> None:
        self.__enabled = True

        self.onEnable()
    
    def disable(self) -> None:
        if self.__hovering:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        
        self.__enabled = False
        self.__pressed = False
        self.__hovering = False

        self.onDisable()
        


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

    def onEnable(self) -> None:
        pass

    def onDisable(self) -> None:
        pass

    @staticmethod
    def setInputLayer(inputLayer : int, resetCursor : bool = True) -> None:
        AbstractButton.__crntInputLayer = inputLayer
        if resetCursor:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)